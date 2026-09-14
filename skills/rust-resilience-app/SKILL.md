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
| [`m-mimalloc-apps`](../../rules/m-mimalloc-apps.md) | HIGH | Configure `mimalloc` as the global allocator in application binaries. |
| [`m-app-error`](../../rules/m-app-error.md) | HIGH | Use `anyhow` for application binaries; never in libraries. |
| [`m-mockable-syscalls`](../../rules/m-mockable-syscalls.md) | HIGH | Design core domain logic "sans I/O" or behind mockable traits. |
| [`m-test-util`](../../rules/m-test-util.md) | MEDIUM | Gate test fixtures and mock clients behind `feature = "test-util"`. |
| [`c-failure`](../../rules/c-failure.md) | HIGH | Mandatory `# Errors`, `# Panics`, and `# Safety` doc sections. |
| [`m-design-for-ai`](../../rules/m-design-for-ai.md) | HIGH | Design code for AI comprehension: strict types and runnable doc tests. |
| [`m-lint-override-expect`](../../rules/m-lint-override-expect.md) | MEDIUM | Use `#[expect]` over `#[allow]` to eliminate zombie lint suppressions. |
