# mem-with-capacity

> Always call `with_capacity()` when the collection size is known or estimable.

## Why It Matters
A `Vec` starts with zero capacity and reallocates geometrically (reallocating and copying elements) as items are pushed. Preallocating performs a single heap allocation.

## Bad
```rust
let mut items = Vec::new();
for i in 0..10_000 {
    items.push(i); // Triggers ~14 reallocations and copies!
}
```

## Good
```rust
let mut items = Vec::with_capacity(10_000);
for i in 0..10_000 {
    items.push(i); // Exactly 1 allocation, 0 reallocations
}
```

## See Also
- [m-box-dst](m-box-dst.md) - Shrink immutable vectors to Boxed slices
- [m-shrink-to-fit](m-shrink-to-fit.md) - Free excess capacity
