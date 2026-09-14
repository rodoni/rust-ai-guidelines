#!/usr/bin/env bash
set -euo pipefail

DEST_DIR="${1:-.}"
echo "==> Setting up OpenCode Rust Guidelines in: $DEST_DIR"

mkdir -p "$DEST_DIR/.opencode/rules"

cp -r rules/* "$DEST_DIR/.opencode/rules/"
cp targets/opencode/AGENTS.md "$DEST_DIR/AGENTS.md"

echo " OpenCode environment configured successfully!"
