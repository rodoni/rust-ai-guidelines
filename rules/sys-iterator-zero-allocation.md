# sys-iterator-zero-allocation

> Chain iterators lazily without intermediate heap allocations until the final consumption point.

## Why It Matters
Calling `.collect::<Vec<_>>()` at each step in a data processing pipeline allocates and reallocates temporary heap buffers, destroys CPU L1 cache locality, and triggers allocator contention. Rust iterators are lazy state machines, so chaining transformations avoids intermediate collections; further fusion, vectorization, or unrolling remain compiler decisions.

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
    // The chain has no intermediate collections; the final `collect` owns the output.
    input
        .iter()
        .copied()
        .filter(|x| x % 2 == 0)
        .filter_map(|x| x.checked_mul(x))
        .filter(|x| *x > 0)
        .collect()
}
```

The final `collect` may still grow the output vector when the iterator cannot
provide an exact size estimate. Measure and reserve capacity separately when
the output size is reliably known.

## When Acceptable
When an intermediate step requires sorting (`.sort()`), random access by index, or borrowing across multiple passes over the transformed dataset.
