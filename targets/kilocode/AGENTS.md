# Kilo Code Rust Guidelines & Agentic Ecosystem

This project adheres to the **Rust AI Guidelines** for low-context, high-soundness Rust development.

## Core Directives
1. **Low-Context Loading**: Reference `.kilo/rules/<rule-id>.md` only on demand. Do not dump extensive documentation into context.
2. **Standard Traits**: Derive `Debug`, `Clone`, `Default`, `Eq`, `Hash` where sound.
3. **Sound Boundaries**: No `unsafe` without an explicit `// SAFETY:` invariant comment.
4. **Error Handling**: Use typed, inspectable errors for libraries, `thiserror` when appropriate, and `anyhow` only for application entrypoints/binaries.
5. **Memory & Allocations**: Preallocate capacity (`with_capacity`) and reuse buffers (`.clear()`).

## Custom Subagents (`.kilo/agents/`)
Specialized subagents available in this project (invocable via `@agent-name` or through delegation):
- **`rust-dev`**: Plans and implements changes, routing to relevant domain skills for APIs, performance, safety, concurrency, and FFI.
- **`rust-reviewer`**: Independently reviews changes and reports evidence-based findings within the inspected scope.
- **`rust-tester`**: Designs and executes behavior-focused tests and workspace-appropriate verification.

## Skills (`.kilo/skills/`)
Modular domain skills loaded on demand:
- `rust-guidelines`: Master rule index and routing hub.
- `rust-api`: API ergonomics and naming conventions.
- `rust-perf`: Performance, memory management, and async stack tuning.
- `rust-concurrency`: Low-level atomics, memory ordering, and synchronization.
- `rust-safety`: Unsafe invariants, FFI soundness, and panic handling.
- `rust-macros`: Declarative and procedural macro conventions.
- `rust-ffi`: Native C-ABI bindings and memory isolation.
- `rust-resilience-app`: Sans-I/O architecture, mockable syscalls, and AI test contracts.
- `rust-agentic-workflow`: Spec-First, TDD, atomic steps, and verification gates.
- `rust-testing`: Unit, integration, property-based, and deterministic async testing.
