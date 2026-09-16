# m-proc-impl

> Separate procedural macro logic into an internal implementation crate with unit tests.

## Why It Matters
A `proc-macro = true` crate can only export procedural macro functions, making direct unit testing of AST transformations difficult. Factoring the AST generator into a separate standard library crate allows normal unit tests.

## Bad
```rust
// In my-derive/src/lib.rs (proc-macro = true)
// All complex AST parsing and token generation stuffed inside proc-macro crate
#[proc_macro_derive(MyTrait)]
pub fn derive_my_trait(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
    // 500 lines of complex syn/quote logic cannot be unit tested with `cargo test`!
}
```

## Good
```rust
// 1. my-derive-internal/src/lib.rs (normal library with unit tests)
pub fn expand_derive(input: syn::DeriveInput) -> syn::Result<proc_macro2::TokenStream> {
    // Testable transformation logic
}

// 2. In my-derive/src/lib.rs (thin proc-macro shim)
#[proc_macro_derive(MyTrait)]
pub fn derive_my_trait(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
    let input = syn::parse_macro_input!(input as syn::DeriveInput);
    my_derive_internal::expand_derive(input)
        .unwrap_or_else(syn::Error::into_compile_error)
        .into()
}
```

## See Also
- [m-example-over-proc](m-example-over-proc.md) - Prefer macro_rules! when possible
- [m-smaller-crates](m-smaller-crates.md) - Decompose into single-responsibility crates
