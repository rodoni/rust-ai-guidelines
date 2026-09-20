# sys-iterator-zero-allocation

> Chain iterators lazily without intermediate heap allocations until the final consumption point.

## Why It Matters
Calling `.collect::<Vec<_>>()` at each step in a data processing pipeline allocates and reallocates temporary heap buffers, destroys CPU L1 cache locality, and triggers allocator contention. Rust iterators are zero-cost lazy state machines; the compiler collapses chained transformations into a single unrolled loop.

## Bad
```rust
pub fn process_records(input: &[i64]) -> Vec<i64> {
    // Allocates a temporary heap vector for every intermediate step!
    let evens: Vec<i64> = input.iter().copied().filter(|x| x % 2 == 0).collect();
    let squares: Vec<i64> = evens.iter().map(|x| x * x).collect();
    let positive: Vec<i64> = squares.into_iter().filter(|x| *x > 0).collect();
    positive
}
```

## Good
```rust
pub fn process_records(input: &[i64]) -> Vec<i64> {
    // Single allocation at the end; rustc compiles this into a tight SIMD-friendly loop!
    input
        .iter()
        .copied()
        .filter(|x| x % 2 == 0)
        .map(|x| x * x)
        .filter(|x| *x > 0)
        .collect()
}
```

## When Acceptable
When an intermediate step requires sorting (`.sort()`), random access by index, or borrowing across multiple passes over the transformed dataset.
