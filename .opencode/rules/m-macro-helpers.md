# m-macro-helpers

> Re-export external third-party dependencies used in macro expansion under `#[doc(hidden)] pub mod _private`.

## Why It Matters
When a declarative or procedural macro expands in a downstream consumer's crate, referencing `$crate::external_dep` fails unless the consumer explicitly adds that dependency to their `Cargo.toml`.

## Bad
```rust
// In my_crate
#[macro_export]
macro_rules! log_event {
    ($msg:expr) => {
        // FAILS if downstream crate does not directly depend on `tracing`!
        tracing::info!($msg);
    };
}
```

## Good
```rust
// In my_crate/src/lib.rs
#[doc(hidden)]
pub mod _private {
    pub use tracing;
}

#[macro_export]
macro_rules! log_event {
    ($msg:expr) => {
        $crate::_private::tracing::info!($msg);
    };
}
```
