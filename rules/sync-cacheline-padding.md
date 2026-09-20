# sync-cacheline-padding

> Consider padding concurrently mutated hot variables to reduce false sharing when measurement and the target architecture justify it.

## Why It Matters
CPUs transfer memory between cores in cache-line granules. When two hot atomics share a cache line, writing to one can invalidate the line for other cores, reducing scalability even when threads access disjoint variables. Cache-line size and the benefit of padding depend on the target and workload.

## Bad
```rust
use std::sync::atomic::AtomicU64;

// Two hot atomics placed adjacent in memory share a single 64-byte cache line!
pub struct MultiThreadStats {
    pub reader_ops: AtomicU64, // Core 0 writes here
    pub writer_ops: AtomicU64, // Core 1 writes here -> ping-pongs cache line!
}
```

## Good
```rust
use crossbeam::utils::CachePadded;
use std::sync::atomic::AtomicU64;

// Solution 1: crossbeam CachePadded ensures separate 64-byte/128-byte cache lines
pub struct MultiThreadStats {
    pub reader_ops: CachePadded<AtomicU64>,
    pub writer_ops: CachePadded<AtomicU64>,
}

// Solution 2: Explicit alignment attribute
#[repr(align(64))]
pub struct IsolatedCounter(pub AtomicU64);
```

## When Acceptable
Structures accessed by a single thread, read-heavy immutable data, or memory-constrained embedded devices do not need cache line padding.
