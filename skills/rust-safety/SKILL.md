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
| [`m-errors-canonical`](../../rules/m-errors-canonical.md) | HIGH | Canonical error structs with backtraces and query methods; avoid leaking error enums. |
| [`c-dtor-fail`](../../rules/c-dtor-fail.md) | CRITICAL | Destructors (`Drop` trait) must never panic. |
| [`m-avoid-statics`](../../rules/m-avoid-statics.md) | HIGH | Avoid mutable global statics; pass state explicitly. |
| [`m-strong-types-guard`](../../rules/m-strong-types-guard.md) | HIGH | Enforce domain invariants upon type construction (*Parse, Don't Validate*). |
| [`atomic-ordering-pair`](../../rules/atomic-ordering-pair.md) | CRITICAL | Choose atomic orderings from the algorithm's synchronization relationship. |
| [`sync-avoid-spinlock`](../../rules/sync-avoid-spinlock.md) | CRITICAL | Avoid unbounded spinning; prefer blocking or bounded adaptive synchronization. |
| [`sync-lock-hierarchy`](../../rules/sync-lock-hierarchy.md) | CRITICAL | Enforce deterministic lock acquisition order to prevent deadlocks. |
| [`er-casts-avoid-as`](../../rules/er-casts-avoid-as.md) | HIGH | Avoid lossy numeric `as` casts; use `TryFrom`/`TryInto` or checked methods. |
| [`er-raii-guard`](../../rules/er-raii-guard.md) | HIGH | Encapsulate state cleanup and resource release into RAII guards (`Drop`). |
