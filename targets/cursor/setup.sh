#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DEST_DIR="${1:-.}"
echo "==> Setting up Cursor Rust Guidelines in: $DEST_DIR"

mkdir -p "$DEST_DIR/.cursor/rules" "$DEST_DIR/.cursor/skills" "$DEST_DIR/.cursor/agents"

# Convert and copy rules as .cursor/rules/*.mdc
for rule in "$REPO_ROOT/rules/"*.md; do
    if [ -f "$rule" ]; then
        rule_name=$(basename "$rule" .md)
        # Extract first line quote (imperative description)
        desc=$(grep -m 1 '^>' "$rule" | sed 's/^>[[:space:]]*//' || echo "Rust AI rule: $rule_name")
        if [ -z "$desc" ]; then
            desc="Rust AI guideline: $rule_name"
        fi
        
        target_file="$DEST_DIR/.cursor/rules/${rule_name}.mdc"
        cat <<EOF > "$target_file"
---
description: ${desc}
globs: "**/*.rs, **/Cargo.toml"
alwaysApply: false
---

EOF
        cat "$rule" >> "$target_file"
    fi
done

# Copy skills
for skill in "$REPO_ROOT/skills/"*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        mkdir -p "$DEST_DIR/.cursor/skills/$skill_name"
        cp -r "$skill"/* "$DEST_DIR/.cursor/skills/$skill_name/"
    fi
done

# Copy specialized subagents
cp -r "$REPO_ROOT/agents/"* "$DEST_DIR/.cursor/agents/"

echo " Cursor environment configured successfully (.cursor/rules/*.mdc)!"
