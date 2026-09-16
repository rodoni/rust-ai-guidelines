#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DEST_DIR="${1:-.}"
echo "==> Setting up Antigravity Rust Guidelines in: $DEST_DIR"

mkdir -p "$DEST_DIR/.agents/skills" "$DEST_DIR/.agents/rules" "$DEST_DIR/.agents/agents"

# Copy rules
cp -r "$REPO_ROOT/rules/"* "$DEST_DIR/.agents/rules/"

# Copy skills
for skill in "$REPO_ROOT/skills/"*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        mkdir -p "$DEST_DIR/.agents/skills/$skill_name"
        cp -r "$skill"/* "$DEST_DIR/.agents/skills/$skill_name/"
    fi
done

# Copy specialized subagents
cp -r "$REPO_ROOT/agents/"* "$DEST_DIR/.agents/agents/"

# Copy guidelines inside .agents/ to keep project root clean
cp "$REPO_ROOT/targets/antigravity/AGENTS.md" "$DEST_DIR/.agents/AGENTS.md"

echo " Antigravity environment configured successfully!"
