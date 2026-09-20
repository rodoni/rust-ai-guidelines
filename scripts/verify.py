#!/usr/bin/env python3
"""
Rust AI Guidelines Verification Suite
Audits rule consistency, structure, link integrity, and deployment across all targets.
"""

import os
import sys
import glob
import re
import tempfile
import subprocess

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

errors = []

def error(msg: str):
    errors.append(msg)
    print(f"\033[1;31m[FAIL]\033[0m {msg}")

def success(msg: str):
    print(f"\033[1;32m[PASS]\033[0m {msg}")

def check_rules_structure():
    print("\n--- 1. Checking Atomic Rules Structure ---")
    rule_files = glob.glob(os.path.join(REPO_ROOT, "rules", "*.md"))
    if not rule_files:
        error("No rule files found in rules/")
        return

    required_sections = ["## Why It Matters", "## Bad", "## Good"]

    for rf in rule_files:
        basename = os.path.splitext(os.path.basename(rf))[0]
        with open(rf, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.strip().splitlines()
        if not lines or not lines[0].startswith(f"# {basename}"):
            error(f"{rf}: First line must be '# {basename}'")

        if not any(line.strip().startswith(">") for line in lines[:5]):
            error(f"{rf}: Missing blockquote imperative '> ...' near the top")

        for sec in required_sections:
            if sec not in content:
                error(f"{rf}: Missing required section '{sec}'")

    success(f"Validated structure of {len(rule_files)} atomic rules.")

def check_rule_references():
    print("\n--- 2. Checking Rule Reference Integrity ---")
    rules_on_disk = {
        os.path.splitext(os.path.basename(f))[0]
        for f in glob.glob(os.path.join(REPO_ROOT, "rules", "*.md"))
    }

    # Check README
    readme_path = os.path.join(REPO_ROOT, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_text = f.read()

    readme_rules = set(re.findall(r'`([a-z0-9-]+)`', readme_text))
    valid_prefixes = ("m-", "c-", "mem-", "unsafe-", "atomic-", "sync-", "er-", "sys-", "wf-")
    readme_rule_candidates = {r for r in readme_rules if r.startswith(valid_prefixes)}
    missing_from_readme = readme_rule_candidates - rules_on_disk
    if missing_from_readme:
        error(f"README.md references non-existent rules: {missing_from_readme}")
    else:
        success("All rules referenced in README.md exist in rules/.")

    # Check Agents
    agent_files = glob.glob(os.path.join(REPO_ROOT, "agents", "*.md"))
    for af in agent_files:
        with open(af, "r", encoding="utf-8") as f:
            text = f.read()
        tokens = set(re.findall(r'`([a-z0-9-]+)`', text))
        candidates = {r for r in tokens if r.startswith(valid_prefixes)}
        missing = candidates - rules_on_disk
        if missing:
            error(f"{af} references non-existent rules: {missing}")

    success(f"Validated rule references across {len(agent_files)} agent specifications.")

    # Check Master Skill Index
    master_skill = os.path.join(REPO_ROOT, "skills", "rust-guidelines", "SKILL.md")
    with open(master_skill, "r", encoding="utf-8") as f:
        master_text = f.read()
    
    indexed_rules = set(re.findall(r'\[`([a-z0-9-]+)`\]\(', master_text))
    unindexed = rules_on_disk - indexed_rules
    if unindexed:
        error(f"Master skill rust-guidelines/SKILL.md is missing index for: {unindexed}")
    else:
        success("All atomic rules are indexed in master skill rust-guidelines/SKILL.md.")

def check_markdown_links():
    print("\n--- 3. Checking Relative Markdown Links ---")
    checked_files = 0
    broken_links = 0

    for folder in ["skills", "agents", "rules", "targets"]:
        for root, _, files in os.walk(os.path.join(REPO_ROOT, folder)):
            for f in files:
                if f.endswith(".md") or f.endswith(".mdc"):
                    checked_files += 1
                    path = os.path.join(root, f)
                    with open(path, "r", encoding="utf-8") as fl:
                        content = fl.read()
                    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                    for text, link in links:
                        if link.startswith(("http://", "https://", "#", "mailto:")):
                            continue
                        clean_link = link.split("#")[0]
                        if not clean_link:
                            continue
                        target = os.path.normpath(os.path.join(root, clean_link))
                        if not os.path.exists(target):
                            error(f"Broken link in {path}: [{text}]({link}) -> {target}")
                            broken_links += 1

    if broken_links == 0:
        success(f"Checked relative links in {checked_files} files (0 broken).")

def check_target_sync():
    print("\n--- 4. Checking Target Synchronization E2E ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        sync_script = os.path.join(REPO_ROOT, "sync.sh")

        # Deploy all
        result = subprocess.run(
            ["bash", sync_script, "all", tmpdir],
            capture_output=True,
            text=True,
            cwd=tmpdir # Run from inside tmpdir to test PWD independence!
        )
        if result.returncode != 0:
            error(f"sync.sh all failed:\n{result.stderr}")
            return

        expected_paths = [
            os.path.join(tmpdir, ".agents", "rules"),
            os.path.join(tmpdir, ".agents", "skills"),
            os.path.join(tmpdir, ".agents", "agents"),
            os.path.join(tmpdir, ".agents", "AGENTS.md"),
            os.path.join(tmpdir, ".opencode", "rules"),
            os.path.join(tmpdir, ".opencode", "skills"),
            os.path.join(tmpdir, ".opencode", "agents"),
            os.path.join(tmpdir, ".opencode", "AGENTS.md"),
            os.path.join(tmpdir, ".kilo", "rules"),
            os.path.join(tmpdir, ".kilo", "skills"),
            os.path.join(tmpdir, ".kilo", "agents"),
            os.path.join(tmpdir, ".kilo", "AGENTS.md"),
            os.path.join(tmpdir, "kilo.jsonc"),
            os.path.join(tmpdir, ".cursor", "rules"),
            os.path.join(tmpdir, ".claude", "rules"),
            os.path.join(tmpdir, "CLAUDE.md"),
            os.path.join(tmpdir, ".github", "copilot-instructions.md"),
        ]

        for p in expected_paths:
            if not os.path.exists(p):
                error(f"Expected deployed path does not exist: {p}")

        # Check clean command
        clean_result = subprocess.run(
            ["bash", sync_script, "clean", "all", tmpdir],
            capture_output=True,
            text=True,
            cwd=tmpdir
        )
        if clean_result.returncode != 0:
            error(f"sync.sh clean all failed:\n{clean_result.stderr}")
        else:
            if os.path.exists(os.path.join(tmpdir, ".agents")) or os.path.exists(os.path.join(tmpdir, ".kilo")):
                error("sync.sh clean all left leftover directories")

        success("sync.sh deploy and clean passed across all targets in isolated temp directory.")

def main():
    print("==============================================")
    print("  Rust AI Guidelines Integrity & CI Suite    ")
    print("==============================================")

    check_rules_structure()
    check_rule_references()
    check_markdown_links()
    check_target_sync()

    print("\n----------------------------------------------")
    if errors:
        print(f"\033[1;31mFAILURE: {len(errors)} error(s) encountered.\033[0m")
        sys.exit(1)
    else:
        print("\033[1;32mSUCCESS: All integrity checks passed!\033[0m")
        sys.exit(0)

if __name__ == "__main__":
    main()
