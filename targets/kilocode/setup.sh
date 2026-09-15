#!/usr/bin/env bash
set -euo pipefail

DEST_DIR="${1:-.}"
echo "==> Setting up Kilo Code Rust Guidelines in: $DEST_DIR"

mkdir -p "$DEST_DIR/.kilo/rules" "$DEST_DIR/.kilo/skills" "$DEST_DIR/.kilo/agents"

# Copy rules
cp -r rules/* "$DEST_DIR/.kilo/rules/"

# Copy skills
for skill in skills/*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        mkdir -p "$DEST_DIR/.kilo/skills/$skill_name"
        cp -r "$skill"/* "$DEST_DIR/.kilo/skills/$skill_name/"
    fi
done

# Copy custom agents/subagents
cp -r agents/* "$DEST_DIR/.kilo/agents/"

# Copy project-level guidelines inside .kilo/ to keep project root clean
cp targets/kilocode/AGENTS.md "$DEST_DIR/.kilo/AGENTS.md"

# Setup kilo.jsonc configuration
if [ ! -f "$DEST_DIR/kilo.jsonc" ]; then
    cp targets/kilocode/kilo.jsonc "$DEST_DIR/kilo.jsonc"
    echo " Created $DEST_DIR/kilo.jsonc with rule instructions"
else
    if ! grep -q "\.kilo/rules" "$DEST_DIR/kilo.jsonc"; then
        echo "⚠️ Notice: $DEST_DIR/kilo.jsonc exists. Ensure \".kilo/rules/*.md\" is included in the \"instructions\" array."
    fi
fi

# Inform about legacy migration if .kilocode directory exists
if [ -d "$DEST_DIR/.kilocode" ]; then
    echo "ℹ️  Note: Legacy .kilocode directory detected. Rules, skills, and agents are now centralized under .kilo/."
fi

echo " Kilo Code environment configured successfully!"
