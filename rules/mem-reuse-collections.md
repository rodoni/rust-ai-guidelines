# mem-reuse-collections

> Clear and reuse existing buffer allocations across iterations instead of allocating new ones.

## Why It Matters
Allocating and dropping collections inside tight loops generates massive allocator pressure and CPU cache churn. `.clear()` retains capacity while resetting length to 0.

## Bad
```rust
for record in stream {
    // New heap allocation every iteration!
    let mut buffer = Vec::new();
    record.serialize_into(&mut buffer);
    sink.write_all(&buffer);
}
```

## Good
```rust
let mut buffer = Vec::with_capacity(1024);
for record in stream {
    buffer.clear(); // Keeps the current capacity; growth may still allocate
    record.serialize_into(&mut buffer);
    sink.write_all(&buffer);
}
```
