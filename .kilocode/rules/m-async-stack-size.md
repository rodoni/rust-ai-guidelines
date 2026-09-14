# m-async-stack-size

> Box large state buffers across `.await` points to avoid giant future frame sizes.

## Why It Matters
When an `async fn` awaits, all local variables alive across the `.await` point become fields in the generated future struct. If an array or heavy struct is kept on the stack across `.await`, the future size balloons, multiplying memory usage across thousands of concurrent tasks.

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
    tokio::time::sleep(Duration::from_millis(10)).await; // Future is only ~16 bytes
    send(&buffer).await;
}
```
