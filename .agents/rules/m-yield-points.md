# m-yield-points

> Insert cooperative yield points in long-running CPU-bound loops in async tasks.

## Why It Matters
Async runtimes (like Tokio) use cooperative multitasking. A CPU-heavy loop that never awaits starves other tasks on the same worker thread, causing tail latency spikes.

## Bad
```rust
async fn hash_large_dataset(items: &[Data]) -> Vec<u64> {
    let mut results = Vec::with_capacity(items.len());
    for item in items {
        results.push(expensive_hash(item)); // Blocks worker thread for 500ms!
    }
    results
}
```

## Good
```rust
async fn hash_large_dataset(items: &[Data]) -> Vec<u64> {
    let mut results = Vec::with_capacity(items.len());
    for (i, item) in items.iter().enumerate() {
        if i % 1000 == 0 {
            tokio::task::yield_now().await; // Cooperatively yields to scheduler
        }
        results.push(expensive_hash(item));
    }
    results
}
```
