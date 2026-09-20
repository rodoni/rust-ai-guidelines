---
name: rust-concurrency
description: >
  Low-level concurrency, atomic memory ordering, lock-free synchronization,
  and deadlock prevention based on Rust Atomics and Locks by Mara Bos.
---

# Rust Concurrency & Atomics Guidelines

Rules for memory ordering (`Acquire`/`Release`), lock-free synchronization, avoiding user-space spinlocks, cache line padding, and deadlock prevention.

## Rules Index

| Rule | Impact | Summary |
|---|---|---|
| [`atomic-ordering-pair`](../../rules/atomic-ordering-pair.md) | CRITICAL | Pair `Release` stores with `Acquire` loads; avoid unjustified `Relaxed` or `SeqCst`. |
| [`atomic-cas-weak-loops`](../../rules/atomic-cas-weak-loops.md) | HIGH | Prefer `compare_exchange_weak` in atomic retry loops. |
| [`sync-avoid-spinlock`](../../rules/sync-avoid-spinlock.md) | CRITICAL | Avoid busy-wait spinlocks in user space; use OS blocking locks or futexes. |
| [`sync-cacheline-padding`](../../rules/sync-cacheline-padding.md) | HIGH | Pad hot atomic variables across threads to avoid false sharing. |
| [`sync-lock-hierarchy`](../../rules/sync-lock-hierarchy.md) | CRITICAL | Enforce deterministic lock acquisition order to mathematically prevent deadlocks. |
