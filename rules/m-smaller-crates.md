# m-smaller-crates

> Decompose monolithic crates into smaller, single-responsibility workspace crates.

## Why It Matters
Giant monolithic crates force Cargo to rebuild entire compilation units whenever any file changes, destroying incremental compilation benefits. Splitting by architectural layers (`-core`, `-ffi`, `-macros`, `-cli`) establishes clear boundary enforcement, simplifies testing, and prevents accidental circular dependencies.

## Bad
```
my-huge-crate/
├── src/
│   ├── ast_macros.rs    # Heavy syn/quote proc-macro logic mixed in
│   ├── c_abi.rs         # Unsafe C-ABI FFI shims mixed with business logic
│   ├── web_handlers.rs  # Axum/Actix web framework endpoints
│   ├── database.rs      # SQLx database connections
│   └── lib.rs           # Massive compile bottleneck
```

## Good
```
my-workspace/
├── crates/
│   ├── my-core/         # Pure domain logic "sans I/O" (fast compilation)
│   ├── my-macros/       # Declarative or internal proc-macro crate
│   ├── my-ffi/          # C-ABI and unsafe interop boundary
│   └── my-server/       # Application binary with HTTP framework
└── Cargo.toml           # Root workspace Cargo.toml
```

## See Also
- [m-cargo-workspace](m-cargo-workspace.md) - Centralize workspace dependency versions
- [m-proc-impl](m-proc-impl.md) - Separate proc macro AST logic into internal crate
- [m-ffi-translates](m-ffi-translates.md) - FFI crates translate types only
