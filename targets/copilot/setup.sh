#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DEST_DIR="${1:-.}"
echo "==> Setting up GitHub Copilot Rust Guidelines in: $DEST_DIR"

mkdir -p "$DEST_DIR/.github"

target_file="$DEST_DIR/.github/copilot-instructions.md"
if [ ! -f "$target_file" ]; then
    cp "$REPO_ROOT/targets/copilot/copilot-instructions.md" "$target_file"
    echo " Created $target_file"
else
    if ! grep -q "Rust AI Guidelines" "$target_file"; then
        echo "" >> "$target_file"
        cat "$REPO_ROOT/targets/copilot/copilot-instructions.md" >> "$target_file"
        echo " Appended Rust AI Guidelines to existing $target_file"
    else
        echo "ℹ️  Existing $target_file already includes Rust AI Guidelines"
    fi
fi

echo " GitHub Copilot instructions configured successfully!"
