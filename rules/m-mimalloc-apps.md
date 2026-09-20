# m-mimalloc-apps

> Evaluate `mimalloc` as a global allocator for application binaries when benchmarks justify it.

## Why It Matters
Allocator performance depends on the target, workload, allocation patterns, latency requirements, and deployment constraints. `mimalloc` can improve some high-concurrency workloads, but it can also increase footprint or regress other workloads.

## Bad
```rust
// Application main with standard default system allocator
fn main() {
    start_server();
}
```

## Good
```rust
// In Cargo.toml: mimalloc = { version = "0.1", default-features = false }

use mimalloc::MiMalloc;

#[global_allocator]
static GLOBAL: MiMalloc = MiMalloc;

fn main() {
    start_server();
}
```

## When Acceptable
Never configure `#[global_allocator]` in library crates. Benchmark representative workloads before enabling it, and configure it only in the root binary (`main.rs`) or an intentionally isolated test harness.
