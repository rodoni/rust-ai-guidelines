# m-shrink-to-fit

> Consider `shrink_to_fit()` for long-lived collections only after measuring their growth pattern.

## Why It Matters
Builders may over-allocate capacity during assembly, but `shrink_to_fit()` can itself reallocate and does not guarantee that the allocator returns memory to the operating system. It is counterproductive when the collection will grow again.

## Bad
```rust
// Left with excess capacity allocated forever
pub struct StaticRegistry {
    routes: HashMap<String, RouteHandler>,
}
```

## Good
```rust
impl StaticRegistryBuilder {
    pub fn build(mut self) -> StaticRegistry {
        self.routes.shrink_to_fit(); // Use only when the collection will remain near this size
        StaticRegistry { routes: self.routes }
    }
}
```
