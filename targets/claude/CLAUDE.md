# Claude Code Rust Guidelines

This repository follows the **Rust AI Guidelines** for low-context, high-soundness Rust development.

## Core Directives
1. **Low-Context Loading**: Reference `.claude/rules/<rule-id>.md` strictly on-demand. Do not dump large documentation into context.
2. **Derive Standard Traits**: Always derive `Debug`, `Clone`, `Default`, `Eq`, `Hash` where sound.
3. **Sound Boundaries**: No `unsafe` without an explicit `// SAFETY:` invariant comment.
4. **Error Handling**: Use canonical typed enums (`thiserror`) for libraries, `anyhow` only for top-level binaries/CLI.
5. **Memory**: Preallocate capacity (`with_capacity`) and reuse buffers (`.clear()`).
6. **Workspace**: Centralize dependencies under `[workspace.dependencies]` in root `Cargo.toml`.

## Available Specialized Roles (`.claude/agents/`)
- `rust-dev`: Plans and implements changes, loading focused skills for APIs, performance, safety, concurrency, errors, and FFI.
- `rust-reviewer`: Independently reviews changes and reports actionable, evidence-based findings within the inspected scope.
- `rust-tester`: Designs and executes behavior-focused tests with deterministic, workspace-appropriate verification.
