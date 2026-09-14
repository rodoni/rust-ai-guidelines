#!/usr/bin/env bash
set -euo pipefail

DEST_DIR="${1:-.}"
echo "==> Setting up Antigravity Rust Guidelines in: $DEST_DIR"

mkdir -p "$DEST_DIR/.agents/skills" "$DEST_DIR/.agents/rules"

# Copy rules
cp -r rules/* "$DEST_DIR/.agents/rules/"

# Copy skills
for skill in skills/*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        mkdir -p "$DEST_DIR/.agents/skills/$skill_name"
        cp -r "$skill"/* "$DEST_DIR/.agents/skills/$skill_name/"
    fi
done

# Copy root AGENTS.md for Antigravity workspace
cp targets/antigravity/AGENTS.md "$DEST_DIR/AGENTS.md"

echo " Antigravity environment configured successfully!"
