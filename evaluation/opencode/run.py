#!/usr/bin/env python3
"""Run the OpenCode evaluation sequentially through its official CLI."""

import argparse
import datetime as dt
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INITIAL = HERE / "fixture" / "initial"
TASKS = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))
PREAMBLE = (
    "Work only in this Rust fixture. Follow the task prompt, inspect relevant "
    "files, and report exact commands and outcomes. Do not claim commands you "
    "did not run.\n\n"
)
CHECKS = [
    ["cargo", "fmt", "--check"],
    ["cargo", "test"],
    ["cargo", "clippy", "--", "-D", "warnings"],
]


def seed_review_target(project: Path, setup: str) -> None:
    source = project / "src" / "lib.rs"
    text = source.read_text(encoding="utf-8")
    if setup == "overflow_sum_mutant":
        before = "values.iter().copied().fold(0, i32::saturating_add)"
        if text.count(before) != 1:
            raise RuntimeError("Overflow mutant no longer matches the fixture")
        source.write_text(text.replace(before, "values.iter().copied().sum()"), encoding="utf-8")
    elif setup == "review_unsafe":
        marker = "#[cfg(test)]\nmod tests {"
        addition = '''/// View `len` elements at `ptr` as a slice.\npub unsafe fn raw_view<'a>(ptr: *const i32, len: usize) -> &'a [i32] {\n    unsafe { std::slice::from_raw_parts(ptr, len) }\n}\n\n'''
        if text.count(marker) != 1:
            raise RuntimeError("REV-2 insertion point no longer matches the fixture")
        source.write_text(text.replace(marker, addition + marker), encoding="utf-8")


def initialize_project(project: Path, task: dict) -> None:
    commands = [
        ["git", "init", "--quiet"],
        ["git", "config", "user.name", "Evaluation Fixture"],
        ["git", "config", "user.email", "evaluation@example.invalid"],
        ["git", "add", "Cargo.toml", "Cargo.lock", "opencode.json", "src/lib.rs"],
        ["git", "commit", "--quiet", "-m", "fixture initial state"],
    ]
    for command in commands:
        result = run_command(command, project, 30)
        if result.returncode != 0:
            raise RuntimeError(f"Fixture Git setup failed: {' '.join(command)}\n{result.stderr}")

    if task.get("setup"):
        seed_review_target(project, task["setup"])
        if task["id"] == "TEST-2":
            result = run_command(["git", "add", "src/lib.rs"], project, 30)
            if result.returncode == 0:
                result = run_command(["git", "commit", "--quiet", "-m", "seed overflow regression"], project, 30)
            if result.returncode != 0:
                raise RuntimeError(f"TEST-2 seed commit failed\n{result.stderr}")


def reported_usage(output: str) -> dict:
    totals = {"input": 0, "output": 0, "reasoning": 0, "cache_read": 0, "cache_write": 0}
    cost = 0.0
    found_usage = False
    found_cost = False
    session_ids = set()
    for line in output.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("sessionID"):
            session_ids.add(event["sessionID"])
        part = event.get("part", {})
        if event.get("type") != "step_finish":
            continue
        tokens = part.get("tokens")
        if isinstance(tokens, dict):
            found_usage = True
            totals["input"] += tokens.get("input", 0)
            totals["output"] += tokens.get("output", 0)
            totals["reasoning"] += tokens.get("reasoning", 0)
            cache = tokens.get("cache", {})
            totals["cache_read"] += cache.get("read", 0)
            totals["cache_write"] += cache.get("write", 0)
        if isinstance(part.get("cost"), (int, float)):
            found_cost = True
            cost += part["cost"]
    return {
        "session_ids": sorted(session_ids),
        "reported_tokens": totals if found_usage else "N/A",
        "reported_cost": cost if found_cost else "N/A",
        "usage_source": "OpenCode JSONL step_finish events" if found_usage or found_cost else "N/A",
    }


def make_jobs(repetitions: int, seed: int, tasks=TASKS, skip_pairs=()):
    rng = random.Random(seed)
    pairs = []
    for task in tasks:
        for repetition in range(1, repetitions + 1):
            pair_conditions = ["A", "B"]
            rng.shuffle(pair_conditions)
            pairs.append((task, repetition, pair_conditions))
    rng.shuffle(pairs)
    jobs = []
    for task, repetition, conditions in pairs:
        if (task["id"], repetition) in skip_pairs:
            continue
        for condition in conditions:
            jobs.append((task, repetition, condition))
    return jobs


def run_preflight(model: str, timeout: int) -> int:
    raw_root = HERE / "results" / "raw" / "preflight"
    raw_root.mkdir(parents=True, exist_ok=True)
    attempt = 1
    while (raw_root / f"attempt-{attempt:02d}").exists():
        attempt += 1
    output_dir = raw_root / f"attempt-{attempt:02d}"
    projects = output_dir / "projects"
    projects.mkdir(parents=True)
    checks = [{"condition": "A", "agent": None}]
    checks.extend(
        {"condition": "B", "agent": agent}
        for agent in dict.fromkeys(task["agent"] for task in TASKS)
    )
    records = []

    for index, check in enumerate(checks, 1):
        run_id = f"P{index:02d}"
        project = projects / run_id
        shutil.copytree(INITIAL, project)
        initialize_project(project, TASKS[0])
        if check["condition"] == "B":
            deploy = run_command(["bash", str(ROOT / "sync.sh"), "opencode", str(project)], ROOT, 120)
            if deploy.returncode != 0:
                raise RuntimeError(f"Preflight deploy failed for {check['agent']}: {deploy.stderr}")
        elif (project / ".opencode").exists():
            raise RuntimeError("Preflight A unexpectedly contains the package")

        command = [
            "opencode", "--standalone", "--print-logs", "--log-level", "info",
            "run", "--model", "invalid/no-such-model", "--format", "json", "--title", run_id,
        ]
        if check["agent"]:
            command.extend(["--agent", check["agent"]])
        command.append("Preflight only. Stop; do not inspect or modify files.")
        result = run_command(command, project, timeout)
        combined = result.stdout + "\n" + result.stderr
        location = re.search(r'location services booted"?\s+directory=([^\s]+)', combined)
        model_rejected = "invalid/no-such-model" in combined and any(
            phrase in combined.lower() for phrase in ("unavailable", "no-route", "not found")
        )
        agent_rejected = "Agent not found" in combined
        isolated = bool(location and Path(location.group(1)).resolve() == project.resolve())
        passed = isolated and model_rejected and not agent_rejected
        (output_dir / f"{run_id}.stdout").write_text(result.stdout, encoding="utf-8")
        (output_dir / f"{run_id}.stderr").write_text(result.stderr, encoding="utf-8")
        records.append({
            "run_id": run_id,
            "condition": check["condition"],
            "agent": check["agent"] or "default",
            "expected_project": str(project.resolve()),
            "logged_project": location.group(1) if location else "N/A",
            "agent_rejected": agent_rejected,
            "invalid_model_rejected_without_provider_route": model_rejected,
            "status": "passed" if passed else "failed",
            "cli_returncode": result.returncode,
        })
        print(f"{run_id}: {check['condition']} {check['agent'] or 'default'} {'PASS' if passed else 'FAIL'}")

    manifest = {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "configured_model_for_future_run": model,
        "comparison": "a-b",
        "probe_model": "invalid/no-such-model (must fail before provider request)",
        "opencode_version": subprocess.run(["opencode", "--version"], text=True, capture_output=True).stdout.strip(),
        "provider_requests": 0,
        "runs": records,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Preflight evidence: {output_dir}")
    return 0 if all(record["status"] == "passed" for record in records) else 1


def latest_preflight_passed() -> bool:
    root = HERE / "results" / "raw" / "preflight"
    manifests = sorted(root.glob("attempt-*/manifest.json"), reverse=True)
    if not manifests:
        return False
    for path in manifests:
        try:
            candidate = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        runs = candidate.get("runs", [])
        if (
            len(runs) == 4
            and {run.get("condition") for run in runs} == {"A", "B"}
            and all(run.get("status") == "passed" for run in runs)
        ):
            return True
    return False


def run_command(command, cwd, timeout):
    environment = os.environ.copy()
    environment["PWD"] = str(Path(cwd).resolve())
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            command,
            124,
            stdout=exc.stdout or "",
            stderr=(exc.stderr or "") + f"\nTimed out after {timeout} seconds\n",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="OpenCode model ID, e.g. openai/gpt-6-luna")
    parser.add_argument("--repetitions", type=int, default=2)
    parser.add_argument("--task", choices=[task["id"] for task in TASKS], help="Limit execution to one task, for a smoke pair")
    parser.add_argument("--skip-pair", action="append", default=[], metavar="TASK:REP", help="Exclude a completed valid pair when continuing a staged run")
    parser.add_argument("--seed", type=int, default=1795289864)
    parser.add_argument("--timeout", type=int, default=900, help="Per-session timeout in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Print the schedule without model calls")
    parser.add_argument("--preflight", action="store_true", help="Verify isolated project and agent discovery without provider calls")
    parser.add_argument("--execute", action="store_true", help="Actually submit sessions to OpenCode")
    args = parser.parse_args()

    if args.repetitions < 1 or args.timeout < 1:
        parser.error("--repetitions and --timeout must be positive")
    skip_pairs = set()
    for value in args.skip_pair:
        try:
            task_id, repetition = value.split(":", 1)
            repetition = int(repetition)
        except ValueError:
            parser.error(f"Invalid --skip-pair {value!r}; expected TASK:REP")
        if task_id not in {task["id"] for task in TASKS} or not 1 <= repetition <= args.repetitions:
            parser.error(f"Unknown task or repetition in --skip-pair {value!r}")
        skip_pairs.add((task_id, repetition))
    if args.task and args.skip_pair:
        parser.error("--task and --skip-pair cannot be combined")
    if sum((args.execute, args.dry_run, args.preflight)) > 1:
        parser.error("--execute, --dry-run, and --preflight are mutually exclusive")
    if not args.execute and not args.dry_run and not args.preflight:
        parser.error("No model calls are made by default; pass --preflight, --dry-run, or --execute")
    if not shutil.which("opencode"):
        parser.error("opencode is not on PATH")

    if args.preflight:
        return run_preflight(args.model, min(args.timeout, 60))
    if args.execute and not latest_preflight_passed():
        parser.error("A successful four-case A/B preflight is required before model calls")

    selected_tasks = [task for task in TASKS if not args.task or task["id"] == args.task]
    jobs = make_jobs(args.repetitions, args.seed, selected_tasks, skip_pairs)
    print(f"Model: {args.model}")
    print(f"Seed: {args.seed}")
    print(f"Planned sessions: {len(jobs)}")
    for index, (task, repetition, condition) in enumerate(jobs, 1):
        agent = task["agent"] if condition == "B" else "default"
        print(f"R{index:03d}  {task['id']} rep={repetition} condition={condition} agent={agent}")
    if args.dry_run:
        return 0

    raw_root = HERE / "results" / "raw"
    raw_root.mkdir(parents=True, exist_ok=True)
    attempt_number = 1
    while (raw_root / f"attempt-{attempt_number:02d}").exists():
        attempt_number += 1
    raw = raw_root / f"attempt-{attempt_number:02d}"
    projects = raw / "projects"
    projects.mkdir(parents=True)
    manifest = {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "model": args.model,
        "provider": args.model.split("/", 1)[0] if "/" in args.model else "N/A",
        "opencode_version": subprocess.run(
            ["opencode", "--version"], text=True, capture_output=True, check=False
        ).stdout.strip(),
        "sampling_parameters": "OpenCode defaults; no per-run override supplied",
        "tool_permissions": "fixture opencode.json: project read/edit, Cargo shell, no external directories",
        "server_mode": "standalone per invocation",
        "seed": args.seed,
        "repetitions": args.repetitions,
        "task_filter": args.task or "all",
        "skipped_pairs": [f"{task}:{rep}" for task, rep in sorted(skip_pairs)],
        "runs": [],
    }
    manifest_path = raw / "manifest.private.json"

    for index, (task, repetition, condition) in enumerate(jobs, 1):
        run_id = f"E{attempt_number:02d}-R{index:03d}"
        project = projects / run_id
        shutil.copytree(INITIAL, project)
        try:
            initialize_project(project, task)
        except RuntimeError as exc:
            manifest["runs"].append({
                "run_id": run_id, "task": task["id"], "repetition": repetition,
                "condition": condition, "status": "fixture_setup_failed",
                "validity": "invalid", "reason": str(exc),
            })
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            print(f"{run_id}: fixture setup failed", flush=True)
            continue

        if condition == "B":
            deploy = run_command(
                ["bash", str(ROOT / "sync.sh"), "opencode", str(project)],
                ROOT,
                120,
            )
            if deploy.returncode != 0:
                (raw / f"{run_id}.deploy.stderr").write_text(deploy.stderr, encoding="utf-8")
                manifest["runs"].append({
                    "run_id": run_id, "task": task["id"], "repetition": repetition,
                    "condition": condition, "status": "deployment_failed",
                    "validity": "invalid", "returncode": deploy.returncode,
                })
                manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                continue
            required = [project / ".opencode" / "AGENTS.md"] + [
                project / ".opencode" / name for name in ("agents", "rules", "skills")
            ]
            if not all(path.exists() for path in required):
                manifest["runs"].append({
                    "run_id": run_id, "task": task["id"], "repetition": repetition,
                    "condition": condition, "status": "deployment_incomplete",
                    "validity": "invalid", "missing_paths": [str(p) for p in required if not p.exists()],
                })
                manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                print(f"{run_id}: incomplete B deployment", flush=True)
                break
        elif (project / ".opencode").exists():
            manifest["runs"].append({
                "run_id": run_id, "task": task["id"], "repetition": repetition,
                "condition": condition, "status": "condition_A_contaminated",
                "validity": "invalid",
            })
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            print(f"{run_id}: A fixture contains .opencode; aborting", flush=True)
            break

        prompt = PREAMBLE + task["prompt"]
        command = [
            "opencode", "--standalone", "--print-logs", "--log-level", "info",
            "run", "--model", args.model, "--format", "json",
            "--title", run_id,
        ]
        if condition == "B":
            command.extend(["--agent", task["agent"]])
        command.append(prompt)

        started = dt.datetime.now(dt.timezone.utc)
        clock = time.monotonic()
        result = run_command(command, project, args.timeout)
        elapsed = time.monotonic() - clock
        ended = dt.datetime.now(dt.timezone.utc)
        combined = result.stdout + "\n" + result.stderr
        location = re.search(r'location services booted"?\s+directory=([^\s]+)', combined)
        root_valid = bool(location and Path(location.group(1)).resolve() == project.resolve())
        agent_missing = "Agent not found" in combined
        (raw / f"{run_id}.jsonl").write_text(result.stdout, encoding="utf-8")
        (raw / f"{run_id}.stderr").write_text(result.stderr, encoding="utf-8")
        record = {
            "run_id": run_id,
            "task": task["id"],
            "repetition": repetition,
            "condition": condition,
            "agent": task["agent"] if condition == "B" else "default",
            "model": args.model,
            "started_at": started.isoformat(),
            "ended_at": ended.isoformat(),
            "elapsed_seconds": round(elapsed, 3),
            "returncode": result.returncode,
            "status": "completed" if result.returncode == 0 and root_valid and not agent_missing else "failed_or_invalid",
            "validity": "valid" if result.returncode == 0 and root_valid and not agent_missing else "invalid",
            "logged_project": location.group(1) if location else "N/A",
            "project_root_verified": root_valid,
            "agent_missing": agent_missing,
            "stdout": f"{run_id}.jsonl",
            "stderr": f"{run_id}.stderr",
            **reported_usage(result.stdout),
        }

        if task["id"].startswith(("DEV-", "TEST-")) and result.returncode == 0:
            check_records = []
            for check in CHECKS:
                checked = run_command(check, project, 300)
                check_records.append({
                    "command": check,
                    "returncode": checked.returncode,
                    "stdout": checked.stdout,
                    "stderr": checked.stderr,
                })
            (raw / f"{run_id}.checks.json").write_text(
                json.dumps(check_records, indent=2) + "\n", encoding="utf-8"
            )
            record["checks"] = f"{run_id}.checks.json"

        manifest["runs"].append(record)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"{run_id}: {record['status']} ({elapsed:.1f}s)", flush=True)
        if record["status"] != "completed":
            print("Aborting after invalid session to avoid further provider calls.", flush=True)
            break

    failures = [run for run in manifest["runs"] if run["status"] != "completed"]
    print(f"Finished: {len(manifest['runs'])} runs; {len(failures)} failed or invalid")
    print(f"Private manifest and raw output: {raw}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
