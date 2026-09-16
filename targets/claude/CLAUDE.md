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
- `rust-lead`: Workspace architecture, crate decomposition, and planning.
- `rust-api-architect`: Ergonomic public APIs, builders, and trait implementations.
- `rust-perf-optimizer`: Memory reuse, fast hashers, and async stack tuning.
- `rust-safety-auditor`: Unsafe soundness, FFI boundaries, and panic-free paths.
- `rust-reviewer`: Clippy `#[expect]` overrides and code hygiene.
