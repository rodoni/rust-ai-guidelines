# mem-with-capacity

> Reserve collection capacity when a reliable estimate makes the allocation worthwhile.

## Why It Matters
A `Vec` may reallocate as items are pushed. A reliable capacity estimate can avoid those reallocations, but an excessive or attacker-controlled estimate increases memory use and latency.

## Bad
```rust
let mut items = Vec::new();
for i in 0..10_000 {
    items.push(i); // Reallocates as needed and copies existing elements
}
```

## Good
```rust
let mut items = Vec::with_capacity(10_000);
for i in 0..10_000 {
    items.push(i); // Avoids growth reallocations when the estimate is sufficient
}
```

## See Also
- [m-box-dst](m-box-dst.md) - Shrink immutable vectors to Boxed slices
- [m-shrink-to-fit](m-shrink-to-fit.md) - Free excess capacity
