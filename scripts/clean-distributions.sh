#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEST_DIR="${1:-$REPO_ROOT}"

if [[ ! -d "$DEST_DIR" ]]; then
    printf 'Error: destination directory does not exist: %s\n' "$DEST_DIR" >&2
    exit 1
fi

directories=(
    ".agents"
    ".opencode"
    ".kilocode"
    ".kilo"
    ".cursor"
    ".claude"
)

files=(
    "AGENTS.md"
    "kilo.jsonc"
    "CLAUDE.md"
    ".github/copilot-instructions.md"
)

for directory in "${directories[@]}"; do
    path="$DEST_DIR/$directory"
    if [[ -e "$path" ]]; then
        rm -rf -- "$path"
        printf 'Removed %s\n' "$path"
    fi
done

for file in "${files[@]}"; do
    path="$DEST_DIR/$file"
    if [[ -e "$path" ]]; then
        rm -f -- "$path"
        printf 'Removed %s\n' "$path"
    fi
done

printf 'Distribution artifacts cleaned from %s\n' "$DEST_DIR"
