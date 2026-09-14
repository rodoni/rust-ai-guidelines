---
name: rust-api
description: >
  API design guidelines based on Rust API Guidelines (C-*) and Microsoft Pragmatic Rust (M-LIBS-*).
  Covers naming conventions, traits, builders, type safety, and ergonomic interface design.
---

# Rust API Design Guidelines

Focused, low-context rules for designing idiomatic, predictable, and robust Rust libraries and public interfaces.

## Rules Index

| Rule | Impact | Summary |
|---|---|---|
| [`c-case`](../../rules/c-case.md) | HIGH | RFC 430 naming conventions. |
| [`c-conv`](../../rules/c-conv.md) | HIGH | `as_` (borrow), `to_` (copy/alloc), `into_` (consume). |
| [`c-getter`](../../rules/c-getter.md) | HIGH | Omit `get_` prefix on standard accessors. |
| [`c-common-traits`](../../rules/c-common-traits.md) | CRITICAL | Eagerly derive `Debug`, `Clone`, `Default`, `Eq`, `Hash`. |
| [`c-send-sync`](../../rules/c-send-sync.md) | CRITICAL | Ensure public types are `Send + Sync` where sound. |
| [`c-newtype`](../../rules/c-newtype.md) | HIGH | Prevent primitive obsession with zero-cost newtypes. |
| [`c-sealed`](../../rules/c-sealed.md) | MEDIUM | Use sealed traits to protect public traits from semver breaks. |
| [`m-weasel-words`](../../rules/m-weasel-words.md) | MEDIUM | Eliminate vague words (`Helper`, `Manager`, `Data`). |
| [`m-regular-fn`](../../rules/m-regular-fn.md) | MEDIUM | Prefer standalone module functions over empty utility structs. |
| [`m-avoid-wrappers`](../../rules/m-avoid-wrappers.md) | HIGH | Never leak `Arc`/`Mutex`/`Box` in public signatures. |
| [`m-di-hierarchy`](../../rules/m-di-hierarchy.md) | HIGH | Concrete types > Generics with bounds > `dyn Trait`. |
| [`m-init-builder`](../../rules/m-init-builder.md) | HIGH | Builder pattern with fallible `.build()` for complex types. |
| [`m-services-clone`](../../rules/m-services-clone.md) | HIGH | Services and client handles are cheaply `Clone` via `Arc`. |
| [`m-async-fn`](../../rules/m-async-fn.md) | MEDIUM | Use native `async fn` syntax instead of returning `impl Future`. |
