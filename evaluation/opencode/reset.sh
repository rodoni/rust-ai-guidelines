#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURE="$SCRIPT_DIR/fixture"

rm -rf "$FIXTURE/work"
mkdir -p "$FIXTURE/work"
cp -R "$FIXTURE/initial/." "$FIXTURE/work/"
