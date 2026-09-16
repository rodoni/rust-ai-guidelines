# m-dont-leak-types

> Do not expose internal foreign crate types in public API signatures without intentional re-exporting.

## Why It Matters
Exposing types from private dependencies in your public API (e.g. returning a `reqwest::Response` or taking `serde_json::Value`) tightly couples your public semver contract to external crates. When that dependency releases a breaking major version, your own library must either make a breaking change or break its users.

## Bad
```rust
// Leaks external dependency type in public signature!
pub fn fetch_data() -> Result<reqwest::Response, reqwest::Error> {
    // Callers are now bound to the exact reqwest minor/major version!
}
```

## Good
```rust
// Expose your own domain types or re-export the dependency intentionally
pub struct HttpResponse {
    pub status: u16,
    pub body: Vec<u8>,
}

pub fn fetch_data() -> Result<HttpResponse, MyCrateError> {
    // Internal use of reqwest is completely hidden
}

// Or if intentionally exposing foreign types, re-export them explicitly:
pub use reqwest;
```

## See Also
- [m-avoid-wrappers](m-avoid-wrappers.md) - Avoid smart pointers in public signatures
- [c-sealed](c-sealed.md) - Sealed traits for semver stability
