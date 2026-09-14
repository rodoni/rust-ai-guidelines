---
name: rust-safety
description: >
  Safety, correctness, unsoundness prevention, unsafe invariants, and panic handling
  based on Microsoft Correctness and Rust API soundness guidelines.
---

# Rust Safety & Correctness Guidelines

Critical rules for guaranteeing memory safety, sound API boundaries, explicit invariants, and structured error handling.

## Rules Index

| Rule | Impact | Summary |
|---|---|---|
| [`unsafe-safety-comment`](../../rules/unsafe-safety-comment.md) | CRITICAL | Mandatory `// SAFETY:` explaining invariants on all `unsafe`. |
| [`unsafe-minimize-scope`](../../rules/unsafe-minimize-scope.md) | CRITICAL | Restrict `unsafe` block strictly to the single triggering expression. |
| [`m-unsound-prevention`](../../rules/m-unsound-prevention.md) | CRITICAL | Safe public APIs wrapping unsafe code must be 100% sound. |
| [`m-panic-on-bug`](../../rules/m-panic-on-bug.md) | CRITICAL | Panics are strictly for bugs; runtime fallibility returns `Result`. |
| [`m-errors-canonical`](../../rules/m-errors-canonical.md) | HIGH | Canonical typed error enums via `thiserror` for libraries. |
