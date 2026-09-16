# Antigravity Rust Guidelines Integration

This file configures the specialized Rust Agentic ecosystem for Google Antigravity.

## Registered Subagents (`.agents/agents/`)
- **`rust-lead`**: Orchestration and architecture planner.
- **`rust-api-architect`**: Public API design and traits.
- **`rust-perf-optimizer`**: Memory and async throughput.
- **`rust-safety-auditor`**: Soundness, unsafe, and FFI.
- **`rust-reviewer`**: Exhaustive compliance, lints, and contract review.

## Available Skills (`.agents/skills/`)
The skills are located under `.agents/skills/`:
- `rust-guidelines`: Master rule index
- `rust-api`: API ergonomics & naming
- `rust-perf`: Performance & memory layout
- `rust-safety`: Unsafe invariants & panic handling
- `rust-macros`: Declarative and proc macros
- `rust-ffi`: Native C-ABI boundaries
- `rust-resilience-app`: Applications, testing & AI guidelines
