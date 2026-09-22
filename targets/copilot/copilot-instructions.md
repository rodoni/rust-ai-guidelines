# GitHub Copilot Instructions for Rust

This project adheres to the **Rust AI Guidelines** for low-context, high-soundness Rust development.

## Core Rules for Code Generation
1. **Naming & Casing (RFC 430)**: UpperCamelCase for types, snake_case for functions/variables, SCREAMING_SNAKE_CASE for consts.
2. **Accessors**: Never prefix getters with `get_`. Use `field()` for immutable access and `field_mut()` for mutable access.
3. **No Leaked Wrappers**: Do not expose `Arc<T>`, `Mutex<T>`, `Rc<T>`, or `Box<T>` in public function parameter or return types. Use `&T`, `&mut T`, or `impl Trait`.
4. **Standard Traits**: Derive `Debug`, `Clone`, `Default`, `Eq`, `Hash` where sound.
5. **Memory & Allocations**:
   - Preallocate capacity with `Vec::with_capacity(n)` or `HashMap::with_capacity(n)` whenever length is known or bounded.
   - Reuse buffers with `.clear()` inside hot loops rather than reallocating.
   - Use `Box<[T]>` or `Box<str>` for immutable owned collections to eliminate the 8-byte capacity field.
6. **Safety & Unsafe**:
   - Any `unsafe` block MUST have a preceding `// SAFETY:` comment explaining why undefined behavior cannot occur.
   - Restrict the `unsafe` block strictly to the single triggering operation.
7. **Error Handling**:
   - In libraries: Use custom typed error enums derived with `thiserror`. Never return `anyhow::Error` or `Box<dyn Error>`.
   - In applications/binaries: Use `anyhow::Result` with `.context()` at the top-level main/CLI boundary.
   - Reserve panics strictly for unrecoverable programming bugs.
8. **Cargo Workspace**:
   - Centralize dependency versions in `[workspace.dependencies]` at the workspace root Cargo.toml.
9. **Testing & Invariants**:
   - Assert specific error variants (`matches!`), never just `.is_err()`.
   - Never use wall-clock `thread::sleep` in tests; use virtual clocks or `tokio::time::pause()`.
   - Use property-based testing (`proptest`) for pure functions, codecs, and domain invariants.

