---
name: rust-perf
description: >
  Performance, memory optimization, zero-copy, and async runtime efficiency rules
  based on Microsoft Rust Performance guidelines and zero-overhead memory patterns.
---

# Rust Performance Guidelines

Rules for reducing allocations, keeping cache locality, minimizing async future footprints, and avoiding CPU stall cycles.

## Rules Index

| Rule | Impact | Summary |
|---|---|---|
| [`mem-with-capacity`](../../rules/mem-with-capacity.md) | HIGH | Preallocate collection capacity when size is known. |
| [`mem-reuse-collections`](../../rules/mem-reuse-collections.md) | HIGH | `.clear()` and reuse buffer allocations inside loops. |
| [`m-box-dst`](../../rules/m-box-dst.md) | HIGH | `Box<[T]>` or `Box<str>` for immutable owned sequences (saves 8B). |
| [`m-shrink-to-fit`](../../rules/m-shrink-to-fit.md) | MEDIUM | Release excess capacity on long-lived structs after construction. |
| [`m-fast-hasher`](../../rules/m-fast-hasher.md) | HIGH | `ahash` or `foldhash` for internal HashMaps (3-5x faster). |
| [`m-async-stack-size`](../../rules/m-async-stack-size.md) | CRITICAL | Box large buffers held across `.await` to shrink future frames. |
| [`m-yield-points`](../../rules/m-yield-points.md) | HIGH | Insert `tokio::task::yield_now()` in CPU-bound async loops. |
| [`sys-struct-field-ordering`](../../rules/sys-struct-field-ordering.md) | HIGH | Order struct fields largest-to-smallest to eliminate padding holes. |
| [`sys-iterator-zero-allocation`](../../rules/sys-iterator-zero-allocation.md) | HIGH | Chain iterators lazily without intermediate heap allocations. |
| [`sys-dispatch-tradeoff`](../../rules/sys-dispatch-tradeoff.md) | HIGH | Static dispatch in hot loops; dynamic dispatch (`dyn`) on cold paths. |
| [`sync-cacheline-padding`](../../rules/sync-cacheline-padding.md) | HIGH | Pad hot atomic variables across threads to avoid false sharing. |
| [`atomic-cas-weak-loops`](../../rules/atomic-cas-weak-loops.md) | HIGH | Prefer `compare_exchange_weak` in atomic retry loops. |
