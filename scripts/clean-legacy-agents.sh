#!/usr/bin/env bash
set -euo pipefail

agent_dir="${1:?usage: clean-legacy-agents.sh <deployed-agent-directory>}"

# Remove only agent files previously shipped by this package.
for agent in rust-lead rust-api-architect rust-perf-optimizer rust-safety-auditor rust-test-engineer; do
    rm -f "$agent_dir/$agent.md"
done
