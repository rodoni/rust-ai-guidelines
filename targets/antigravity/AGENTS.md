# Antigravity Rust Guidelines Integration

This file configures the specialized Rust Agentic ecosystem for Google Antigravity.

## Registered Subagents (`.agents/agents/`)
- **`rust-dev`**: Plans and implements Rust changes, routing to API, performance, safety, concurrency, and FFI skills as needed.
- **`rust-reviewer`**: Independently reviews changes and reports evidence-based, actionable findings within the available scope.
- **`rust-tester`**: Designs and runs behavior-focused tests with workspace-appropriate verification.

## Available Skills (`.agents/skills/`)
The skills are located under `.agents/skills/`:
- `rust-guidelines`: Master rule index
- `rust-api`: API ergonomics & naming
- `rust-perf`: Performance & memory layout
- `rust-concurrency`: Low-level atomics, memory ordering & synchronization
- `rust-safety`: Unsafe invariants & panic handling
- `rust-macros`: Declarative and proc macros
- `rust-ffi`: Native C-ABI boundaries
- `rust-resilience-app`: Applications, testing & AI guidelines
- `rust-agentic-workflow`: Spec-First, TDD, atomic steps & verification gates
- `rust-testing`: Unit, integration, property-based & async testing
