# OpenCode Agent Instructions

Instructions for OpenCode / OpenCodeInterpreter working with Rust repositories.

## Low-Context Guidelines Protocol
Before generating or refactoring Rust code, refer to the atomic rule files under `.opencode/rules/` (or `rules/`). Do not load entire books into context; load only the specific rule ID needed for the task.

### Available Agents / Personas (`.opencode/agents/`)
- **`rust-lead`**: High-level triage, modular workspace architecture, and planning.
- **`rust-api-architect`**: Follows `c-case`, `c-conv`, `c-getter`, `c-common-traits`, `m-avoid-wrappers`, `m-init-builder`.
- **`rust-perf-optimizer`**: Follows `mem-with-capacity`, `mem-reuse-collections`, `m-box-dst`, `m-fast-hasher`.
- **`rust-safety-auditor`**: Follows `unsafe-safety-comment`, `unsafe-minimize-scope`, `m-unsound-prevention`, `m-panic-on-bug`.
- **`rust-reviewer`**: Follows `m-lint-override-expect`, `c-failure`, `m-design-for-ai`.

### Modular Skills (`.opencode/skills/`)
Domain skill sets available for on-demand inspection:
- `rust-guidelines`: Master index and routing hub.
- `rust-api`: API ergonomics and naming conventions.
- `rust-perf`: Performance, memory management, and async stack tuning.
- `rust-concurrency`: Low-level atomics, memory ordering, and synchronization.
- `rust-safety`: Unsafe invariants, FFI soundness, and panic handling.
- `rust-macros`: Declarative and procedural macro conventions.
- `rust-ffi`: Native C-ABI bindings and memory isolation.
- `rust-resilience-app`: Sans-I/O architecture, mockable syscalls, and AI test contracts.
- `rust-agentic-workflow`: Spec-First, TDD, atomic steps, and verification gates.
