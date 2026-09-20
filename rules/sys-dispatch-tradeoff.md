# sys-dispatch-tradeoff

> Weigh static and dynamic dispatch against code size, compile time, workload, and API ergonomics.

## Why It Matters
Generics (`impl Trait`, `T: Trait`) monomorphize code, which can enable inlining and specialization at the cost of larger binaries and longer compile times. Dynamic dispatch (`&dyn Trait`, `Box<dyn Trait>`) adds an indirect call and shares machine code. The trade-off depends on hardware, workload, code size, compile time, nesting, and API ergonomics; it is useful beyond only plugins or heterogeneous collections.

## Bad
```rust
// Extreme 1: Indiscriminate monomorphization creates explosive code bloat!
pub fn handle_event_heavy<E: Trait1 + Trait2 + Trait3 + Trait4>(event: E) {
    // 500 lines of complex logic monomorphized 40 times -> megabytes of duplicated machine code
}

// Extreme 2: Dynamic dispatch in microsecond inner loops
pub fn sum_numbers(items: &[Box<dyn Number>]) -> f64 {
    // Vtable lookup on every element in tight loop stalls CPU pipeline!
    items.iter().map(|n| n.as_f64()).sum()
}
```

## Good
```rust
// Hot path: static dispatch enables inlining and SIMD
pub fn sum_numbers<T: Number>(items: &[T]) -> f64 {
    items.iter().map(|n| n.as_f64()).sum()
}

// Cold/orchestration path: dynamic dispatch prevents binary bloat
pub fn dispatch_event(handler: &dyn EventHandler, payload: &[u8]) {
    handler.handle(payload);
}
```

## When Acceptable
Heterogeneous collections (e.g., storing different shapes in `Vec<Box<dyn Shape>>`) inherently require dynamic dispatch.
