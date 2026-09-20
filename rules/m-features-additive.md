# m-features-additive

> Prefer additive Cargo features; make mutually exclusive features explicit and diagnosable.

## Why It Matters
Cargo unifies features across the dependency graph. Features should normally add capabilities without changing existing APIs or silently disabling code. A crate with genuinely exclusive backends may use mutually exclusive features, but must document the constraint and reject invalid combinations clearly.

## Bad
```toml
# In Cargo.toml
[features]
# Anti-pattern: mutually exclusive features with no documented constraint!
backend-a = []
backend-b = [] # Mutually exclusive with backend-a
```
```rust
// Without a diagnostic, the invalid combination fails ambiguously or changes APIs.
#[cfg(feature = "backend-a")]
pub use backend_a::Client;

#[cfg(feature = "backend-b")]
pub use backend_b::Client;
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
