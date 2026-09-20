---
name: rust-resilience-app
description: >
  Guidelines for applications, testability, sans I/O architecture, doc contracts,
  and AI-friendly code design based on Microsoft Apps, Resilience, and AI chapters.
---

# Rust Resilience, Applications & AI Guidelines

Engineering standards for robust binaries, mockable system boundaries, strict documentation contracts, and AI agent optimization.

## Rules Index

| Rule | Impact | Summary |
|---|---|---|
| [`m-mimalloc-apps`](../../rules/m-mimalloc-apps.md) | HIGH | Evaluate `mimalloc` when representative benchmarks justify it. |
| [`m-cargo-workspace`](../../rules/m-cargo-workspace.md) | HIGH | Centralize all dependency versions under `[workspace.dependencies]`. |
| [`m-smaller-crates`](../../rules/m-smaller-crates.md) | HIGH | Decompose monolithic crates into single-responsibility workspace crates. |
| [`m-app-error`](../../rules/m-app-error.md) | HIGH | Use `anyhow` for application binaries; never in libraries. |
| [`m-mockable-syscalls`](../../rules/m-mockable-syscalls.md) | HIGH | Design core domain logic "sans I/O" or behind mockable traits. |
| [`m-test-util`](../../rules/m-test-util.md) | MEDIUM | Gate test fixtures and mock clients behind `feature = "test-util"`. |
| [`c-failure`](../../rules/c-failure.md) | HIGH | Document `# Errors`, `# Panics`, and `# Safety` when applicable. |
| [`m-design-for-ai`](../../rules/m-design-for-ai.md) | HIGH | Design code for AI comprehension: strict types and runnable doc tests. |
| [`m-lint-override-expect`](../../rules/m-lint-override-expect.md) | MEDIUM | Use `#[expect]` over `#[allow]` to eliminate zombie lint suppressions. |
| [`m-log-not-print`](../../rules/m-log-not-print.md) | HIGH | Use telemetry for diagnostics; reserve stdout/stderr for deliberate CLI presentation. |
| [`m-log-structured`](../../rules/m-log-structured.md) | HIGH | Structured telemetry with key-value fields rather than string interpolation. |
| [`m-features-additive`](../../rules/m-features-additive.md) | HIGH | Prefer additive features; diagnose valid exclusive backend combinations. |
