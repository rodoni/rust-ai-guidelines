#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DEST_DIR="${1:-.}"
echo "==> Setting up Claude Code Rust Guidelines in: $DEST_DIR"

mkdir -p "$DEST_DIR/.claude/rules" "$DEST_DIR/.claude/skills" "$DEST_DIR/.claude/agents"

# Copy rules
cp -r "$REPO_ROOT/rules/"* "$DEST_DIR/.claude/rules/"

# Copy skills
for skill in "$REPO_ROOT/skills/"*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        mkdir -p "$DEST_DIR/.claude/skills/$skill_name"
        cp -r "$skill"/* "$DEST_DIR/.claude/skills/$skill_name/"
    fi
done

# Copy custom agents/personas
cp -r "$REPO_ROOT/agents/"* "$DEST_DIR/.claude/agents/"

# Configure CLAUDE.md non-destructively
if [ ! -f "$DEST_DIR/CLAUDE.md" ]; then
    cp "$REPO_ROOT/targets/claude/CLAUDE.md" "$DEST_DIR/CLAUDE.md"
    echo " Created $DEST_DIR/CLAUDE.md"
else
    if ! grep -q "Rust AI Guidelines" "$DEST_DIR/CLAUDE.md"; then
        echo "" >> "$DEST_DIR/CLAUDE.md"
        cat "$REPO_ROOT/targets/claude/CLAUDE.md" >> "$DEST_DIR/CLAUDE.md"
        echo " Appended Rust AI Guidelines section to existing $DEST_DIR/CLAUDE.md"
    else
        echo "ℹ️  Existing $DEST_DIR/CLAUDE.md already includes Rust AI Guidelines"
    fi
fi

echo " Claude Code environment configured successfully!"
