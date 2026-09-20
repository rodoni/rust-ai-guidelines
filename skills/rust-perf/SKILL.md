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
| [`mem-with-capacity`](../../rules/mem-with-capacity.md) | HIGH | Reserve capacity when a reliable estimate makes it worthwhile. |
| [`mem-reuse-collections`](../../rules/mem-reuse-collections.md) | HIGH | `.clear()` and reuse buffer allocations inside loops. |
| [`m-box-dst`](../../rules/m-box-dst.md) | HIGH | Consider `Box<[T]>` or `Box<str>` for frequently instantiated, immutable internal sequences. |
| [`m-shrink-to-fit`](../../rules/m-shrink-to-fit.md) | MEDIUM | Consider releasing excess capacity after measuring long-lived collection growth. |
| [`m-fast-hasher`](../../rules/m-fast-hasher.md) | HIGH | Benchmark faster hashers for internal HashMaps with trusted keys. |
| [`m-async-stack-size`](../../rules/m-async-stack-size.md) | CRITICAL | Measure and reduce large state held across `.await`; boxing is one option. |
| [`m-yield-points`](../../rules/m-yield-points.md) | HIGH | Insert `tokio::task::yield_now()` in CPU-bound async loops. |
| [`sys-struct-field-ordering`](../../rules/sys-struct-field-ordering.md) | HIGH | Order fields deliberately in layout-sensitive performance-critical structs. |
| [`sys-iterator-zero-allocation`](../../rules/sys-iterator-zero-allocation.md) | HIGH | Chain iterators lazily without intermediate heap allocations. |
| [`sys-dispatch-tradeoff`](../../rules/sys-dispatch-tradeoff.md) | HIGH | Weigh static and dynamic dispatch against code size, compile time, workload, and ergonomics. |
| [`sync-cacheline-padding`](../../rules/sync-cacheline-padding.md) | HIGH | Consider padding concurrently mutated hot variables to reduce false sharing when justified. |
| [`atomic-cas-weak-loops`](../../rules/atomic-cas-weak-loops.md) | HIGH | Prefer `compare_exchange_weak` in atomic retry loops. |
