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
| [`atomic-ordering-pair`](../../rules/atomic-ordering-pair.md) | CRITICAL | Choose atomic orderings from the algorithm's synchronization relationship. |
| [`atomic-cas-weak-loops`](../../rules/atomic-cas-weak-loops.md) | HIGH | Prefer `compare_exchange_weak` in atomic retry loops. |
| [`sync-avoid-spinlock`](../../rules/sync-avoid-spinlock.md) | CRITICAL | Avoid unbounded spinning; prefer blocking or bounded adaptive synchronization. |
| [`sync-cacheline-padding`](../../rules/sync-cacheline-padding.md) | HIGH | Consider padding concurrently mutated hot variables to reduce false sharing when justified. |
| [`sync-lock-hierarchy`](../../rules/sync-lock-hierarchy.md) | CRITICAL | Enforce deterministic lock acquisition order to prevent deadlocks. |
