# m-features-additive

> Cargo features must be strictly additive; enabling a feature must never disable functionality or break code.

## Why It Matters
Cargo unifies features across the entire dependency graph. If crate A enables feature `foo` and crate B does not, Cargo builds your crate with `foo` enabled for both. If enabling a feature mutates public API signatures or disables code, it will unpredictably break other crates in the dependency tree.

## Bad
```toml
# In Cargo.toml
[features]
# Anti-pattern: mutually exclusive features!
backend-a = []
backend-b = [] # Mutually exclusive with backend-a
```
```rust
// Code compiles ONLY if exactly one feature is chosen:
#[cfg(all(feature = "backend-a", feature = "backend-b"))]
compile_error!("Features backend-a and backend-b cannot be used together!");
```

## Good
```toml
# In Cargo.toml
[features]
default = ["std"]
std = []
serde = ["dep:serde"]
tokio = ["dep:tokio"]
```
```rust
// Additive features: functionality expands without breaking base API
pub struct Client {
    // base functionality always works
}

#[cfg(feature = "serde")]
impl<'de> serde::Deserialize<'de> for Client { ... }
```

## See Also
- [m-cargo-workspace](m-cargo-workspace.md) - Centralized workspace dependencies
- [m-smaller-crates](m-smaller-crates.md) - Modular crate architecture
