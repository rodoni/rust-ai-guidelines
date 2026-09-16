# m-cargo-workspace

> Centralize all dependency versions under `[workspace.dependencies]` at the workspace root.

## Why It Matters
When member crates declare their own dependency versions independently, version drift inevitably occurs. This causes multiple incompatible versions of the same crate to be compiled into the binary, bloating build times, increasing binary size, and triggering cryptic type-mismatch compiler errors.

## Bad
```toml
# In crates/auth/Cargo.toml
[dependencies]
serde = { version = "1.0.195", features = ["derive"] }
tokio = "1.35.1"

# In crates/api/Cargo.toml
[dependencies]
serde = "1.0.180" # Version drift! Duplicate compilation
tokio = { version = "1.30.0", features = ["full"] }
```

## Good
```toml
# At workspace root Cargo.toml
[workspace.dependencies]
serde = { version = "1.0.210", features = ["derive"] }
tokio = { version = "1.40.0", features = ["rt-multi-thread", "macros"] }

# In crates/auth/Cargo.toml & crates/api/Cargo.toml
[dependencies]
serde.workspace = true
tokio.workspace = true
```

## See Also
- [m-smaller-crates](m-smaller-crates.md) - Split monolithic crates into modular crates
