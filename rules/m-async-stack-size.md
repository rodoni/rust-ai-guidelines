# m-async-stack-size

> Measure and reduce large state held across `.await` points; boxing is one possible technique.

## Why It Matters
When an `async fn` awaits, local variables alive across the `.await` point contribute to the generated future state. Large values can increase memory usage across many concurrent tasks. Measure hot futures and consider shortening lifetimes, extracting preparation into a regular function, or boxing only when the allocation trade-off is justified.

## Bad
```rust
async fn process_chunk() {
    let buffer = [0u8; 64 * 1024]; // 64 KB on stack
    tokio::time::sleep(Duration::from_millis(10)).await; // Future is >64 KB!
    send(&buffer).await;
}
```

## Good
```rust
async fn process_chunk() {
    let buffer = vec![0u8; 64 * 1024].into_boxed_slice(); // Heap-allocated
    tokio::time::sleep(Duration::from_millis(10)).await; // The buffer stays on the heap
    send(&buffer).await;
}
```
