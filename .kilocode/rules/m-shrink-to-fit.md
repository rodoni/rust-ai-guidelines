# m-shrink-to-fit

> Call `shrink_to_fit()` on long-lived collections after construction.

## Why It Matters
Builders often over-allocate capacity during assembly. If the resulting struct lives for the duration of the process, unused spare capacity is wasted RAM.

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
        self.routes.shrink_to_fit(); // Releases spare memory back to allocator
        StaticRegistry { routes: self.routes }
    }
}
```
