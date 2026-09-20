# er-reexport-dependencies

> Re-export types from third-party crates when they appear in your crate's public API surface.

## Why It Matters
When a public function or struct exposes a type from a dependency (e.g., `url::Url`, `http::HeaderMap`), consumers that directly construct or manipulate that type need a compatible version. Re-exporting gives consumers a canonical path and makes the intended dependency version easier to use, but does not make unrelated crate versions compatible.

## Bad
```rust
// Cargo.toml has `reqwest = "0.11"` as a dependency
pub struct Client;

impl Client {
    // Exposes reqwest::Certificate directly without re-exporting it
    pub fn add_root_certificate(&mut self, cert: reqwest::Certificate) {
        // ...
    }
}
// Downstream consumers cannot easily construct `Certificate` without matching your exact version!
```

## Good
```rust
// Re-export the foreign type in your public crate root or relevant module
pub use reqwest::Certificate;

pub struct Client;

impl Client {
    pub fn add_root_certificate(&mut self, cert: Certificate) {
        // ...
    }
}
// Downstream code can use `my_crate::Certificate` reliably
```

## When Acceptable
Crate-internal types or types concealed inside private implementations that never appear in public method signatures or trait definitions.
