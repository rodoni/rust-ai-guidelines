# c-generic

> Minimize assumptions about function parameters by taking flexible generic bounds (`AsRef`, `Into`, `Borrow`).

## Why It Matters
Forcing callers to pass exact concrete types (like `&PathBuf` or `String`) introduces friction and forces needless heap allocations (e.g. `.to_string()`). Generic bounds like `impl AsRef<Path>` or `impl Into<String>` allow callers to pass `&str`, `&Path`, or `String` directly.

## Bad
```rust
// Forces caller to allocate a String and construct a PathBuf
pub fn open_config(filename: PathBuf, name: String) {
    // ...
}

// Awkward call site:
open_config(PathBuf::from("config.json"), "app".to_string());
```

## Good
```rust
use std::path::Path;

// Highly flexible and ergonomic
pub fn open_config(
    filename: impl AsRef<Path>,
    name: impl Into<String>,
) {
    let _path = filename.as_ref();
    let _name = name.into();
    // ...
}

// Clean and frictionless call site:
open_config("config.json", "app");
```

## See Also
- [c-conv-traits](c-conv-traits.md) - Standard conversion traits
- [m-di-hierarchy](m-di-hierarchy.md) - Monomorphization vs dynamic dispatch
