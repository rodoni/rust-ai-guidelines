# m-mimalloc-apps

> Configure `mimalloc` as the global memory allocator in application binaries.

## Why It Matters
The standard system allocator (glibc malloc on Linux, MSVCRT on Windows) suffers from lock contention and memory fragmentation under high-concurrency multi-threaded Rust workloads. `mimalloc` routinely yields 10–30% throughput gains.

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
Never configure `#[global_allocator]` in library crates—only in the root binary (`main.rs`) or integration test harness.
