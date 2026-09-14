#!/usr/bin/env bash
set -euo pipefail

DEST_DIR="${1:-.}"
echo "==> Setting up Kilo Code Rust Guidelines in: $DEST_DIR"

mkdir -p "$DEST_DIR/.kilocode/rules"

cp -r rules/* "$DEST_DIR/.kilocode/rules/"
cp targets/kilocode/instructions.md "$DEST_DIR/.kilocode/instructions.md"

echo " Kilo Code environment configured successfully!"
