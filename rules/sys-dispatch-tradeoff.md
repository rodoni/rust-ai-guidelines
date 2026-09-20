# sys-dispatch-tradeoff

> Use static dispatch for tight loops and hot paths; use dynamic dispatch (`dyn Trait`) to curtail binary bloat and compile times on cold paths.

## Why It Matters
Generics (`impl Trait`, `T: Trait`) monomorphize code, enabling inline expansion, vectorization, and devirtualization at the cost of larger binary sizes and longer compile times. Dynamic dispatch (`&dyn Trait`, `Box<dyn Trait>`) incurs an indirect vtable jump (~1-3ns), but shares machine code and dramatically speeds up compilation for plugin architectures and heterogeneous collections.

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
