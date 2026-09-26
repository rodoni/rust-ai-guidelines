# m-dont-leak-types

> Do not expose internal foreign crate types in public API signatures; encapsulate them in domain types.

## Why It Matters
Exposing types from private dependencies in your public API (e.g. returning a `reqwest::Response` or taking `serde_json::Value`) tightly couples your public semver contract to external crates (Microsoft Pragmatic Rust `M-DONT-LEAK-TYPES`). When that dependency releases a breaking major version, your own library must either make a breaking change or break its users.

## Bad
```rust
// Leaks external dependency type in public signature!
pub fn fetch_data() -> Result<reqwest::Response, reqwest::Error> {
    // Callers are now bound to the exact reqwest minor/major version!
}
```

## Good
```rust
// Encapsulate external types in your own domain types:
pub struct HttpResponse {
    pub status: u16,
    pub body: Vec<u8>,
}

pub fn fetch_data() -> Result<HttpResponse, MyCrateError> {
    // Internal use of reqwest is completely hidden and insulated
}
```

## When Acceptable
If a third-party type is an intentional part of your crate's public contract, re-export that dependency type explicitly so consumers have a guaranteed compatible type path (see [er-reexport-dependencies](er-reexport-dependencies.md)).

## See Also
- [m-avoid-wrappers](m-avoid-wrappers.md) - Avoid smart pointers in public signatures
- [er-reexport-dependencies](er-reexport-dependencies.md) - Re-export third-party types when intentionally exposed
- [c-sealed](c-sealed.md) - Sealed traits for semver stability
