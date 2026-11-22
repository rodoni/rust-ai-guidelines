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
EXPECTED_AGENTS = {"rust-dev", "rust-reviewer", "rust-tester"}
LEGACY_AGENTS = {
    "rust-lead", "rust-api-architect", "rust-perf-optimizer",
    "rust-safety-auditor", "rust-test-engineer",
}
AGENT_TARGET_DIRS = {
    "antigravity": ".agents/agents",
    "opencode": ".opencode/agents",
    "kilocode": ".kilo/agents",
    "cursor": ".cursor/agents",
    "claude": ".claude/agents",
}

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
    valid_prefixes = ("m-", "c-", "mem-", "unsafe-", "atomic-", "sync-", "er-", "sys-", "wf-", "test-")
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

    catalog_links = set(re.findall(r'\[`([a-z0-9-]+)`\]\(rules/[^)]+\)', readme_text))
    if catalog_links != rules_on_disk:
        error(f"README rule catalog mismatch: missing={rules_on_disk - catalog_links}, extra={catalog_links - rules_on_disk}")
    else:
        success(f"README catalog indexes all {len(rules_on_disk)} rule files.")

def check_agents():
    print("\n--- Checking Agent Set and Operational References ---")
    agent_dir = os.path.join(REPO_ROOT, "agents")
    agent_files = {os.path.splitext(os.path.basename(path))[0]
                   for path in glob.glob(os.path.join(agent_dir, "*.md"))}
    if agent_files != EXPECTED_AGENTS:
        error(f"Expected exactly {sorted(EXPECTED_AGENTS)} in agents/, found {sorted(agent_files)}")

    for agent in EXPECTED_AGENTS:
        path = os.path.join(agent_dir, f"{agent}.md")
        if not os.path.isfile(path):
            error(f"Missing agent definition: {path}")
            continue
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if not re.search(rf"(?m)^name:\s*{re.escape(agent)}\s*$", text):
            error(f"{path} frontmatter name does not match {agent}")

    persona_docs = [
        "targets/antigravity/AGENTS.md", "targets/opencode/AGENTS.md",
        "targets/kilocode/AGENTS.md", "targets/claude/CLAUDE.md",
        "targets/copilot/copilot-instructions.md",
    ]
    for relative_path in persona_docs:
        path = os.path.join(REPO_ROOT, relative_path)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        missing = {agent for agent in EXPECTED_AGENTS if f"`{agent}`" not in text and f"{agent}" not in text}
        if missing:
            error(f"{relative_path} does not document personas: {sorted(missing)}")

    operational_roots = ["README.md", "targets", "scripts", "sync.sh", "agents"]
    for entry in operational_roots:
        path = os.path.join(REPO_ROOT, entry)
        paths = [path] if os.path.isfile(path) else glob.glob(os.path.join(path, "**", "*"), recursive=True)
        for candidate in paths:
            if not os.path.isfile(candidate) or os.path.basename(candidate) in {
                "clean-legacy-agents.sh", "verify.py"
            }:
                continue
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    text = f.read()
            except (UnicodeDecodeError, OSError):
                continue
            for legacy in LEGACY_AGENTS:
                if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(legacy)}(?![A-Za-z0-9_-])", text):
                    error(f"Obsolete operational agent reference {legacy} in {candidate}")

    success("Source agent IDs and operational references checked.")

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
    print("\n--- Checking Deployment Ownership and Integration ---")
    result = subprocess.run([sys.executable, os.path.join(REPO_ROOT, "scripts", "test_deployment.py")])
    if result.returncode:
        error("Deployment regression tests failed")
    else:
        success("Deployment regression tests passed")


def main():
    print("==============================================")
    print("  Rust AI Guidelines Integrity & CI Suite    ")
    print("==============================================")

    check_rules_structure()
    check_rule_references()
    check_agents()
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
