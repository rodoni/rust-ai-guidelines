#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-help}"
DEST="${2:-.}"

usage() {
    cat <<EOF
Usage: ./sync.sh <target> [destination_path]

Available targets:
  antigravity  Deploy to Antigravity (.agents/skills/ and .agents/rules/)
  opencode     Deploy to OpenCode (.opencode/rules/ and AGENTS.md)
  kilocode     Deploy to Kilo Code (.kilocode/rules/ and instructions.md)
  all          Deploy to all targets simultaneously
  help         Show this help message

Examples:
  ./sync.sh antigravity
  ./sync.sh opencode /path/to/my-rust-project
  ./sync.sh all .
EOF
}

case "$TARGET" in
    antigravity)
        bash targets/antigravity/setup.sh "$DEST"
        ;;
    opencode)
        bash targets/opencode/setup.sh "$DEST"
        ;;
    kilocode)
        bash targets/kilocode/setup.sh "$DEST"
        ;;
    all)
        bash targets/antigravity/setup.sh "$DEST"
        bash targets/opencode/setup.sh "$DEST"
        bash targets/kilocode/setup.sh "$DEST"
        echo " All targets synchronized successfully in $DEST!"
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        echo "Unknown target: $TARGET"
        usage
        exit 1
        ;;
esac
