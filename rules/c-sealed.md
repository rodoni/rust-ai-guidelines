# c-sealed

> Seal public traits only when the crate must control their implementations.

## Why It Matters
Public traits that downstream crates implement cannot have new required methods added in minor releases without breaking semver. Sealing prevents downstream implementations while exposing the trait for generic bounds, but it also prevents external mocks, plugins, and legitimate integrations.

## Bad
```rust
// Public trait: any new method breaks downstream crates!
pub trait Transport {
    fn send(&self, bytes: &[u8]);
}
```

## Good
```rust
mod private {
    pub trait Sealed {}
}

// Sealed trait: only types in this crate can implement it
pub trait Transport: private::Sealed {
    fn send(&self, bytes: &[u8]);
}

pub struct TcpTransport;
impl private::Sealed for TcpTransport {}
impl Transport for TcpTransport {
    fn send(&self, bytes: &[u8]) { ... }
}
```
