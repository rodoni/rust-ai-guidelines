# Antigravity Rust Guidelines Integration

This file configures the specialized Rust Agentic ecosystem for Google Antigravity.

## Registered Subagents
- **`rust-lead`**: Orchestration and architecture planner ([agents/rust-lead.md](../../agents/rust-lead.md)).
- **`rust-api-architect`**: Public API design and traits ([agents/rust-api-architect.md](../../agents/rust-api-architect.md)).
- **`rust-perf-optimizer`**: Memory and async throughput ([agents/rust-perf-optimizer.md](../../agents/rust-perf-optimizer.md)).
- **`rust-safety-auditor`**: Soundness, unsafe, and FFI ([agents/rust-safety-auditor.md](../../agents/rust-safety-auditor.md)).
- **`rust-reviewer`**: Lints and checklist review ([agents/rust-reviewer.md](../../agents/rust-reviewer.md)).

## Available Skills
The skills are located under `.agents/skills/`:
- `rust-guidelines`: Master rule index
- `rust-api`: API ergonomics & naming
- `rust-perf`: Performance & memory layout
- `rust-safety`: Unsafe invariants & panic handling
- `rust-macros`: Declarative and proc macros
- `rust-ffi`: Native C-ABI boundaries
- `rust-resilience-app`: Applications, testing & AI guidelines
