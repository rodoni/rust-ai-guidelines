# m-proc-impl

> Separate procedural macro logic into an internal implementation crate with unit tests.

## Why It Matters
A `proc-macro = true` crate can only export procedural macro functions, making direct unit testing of AST transformations difficult. Factoring the AST generator into a separate standard library crate allows normal unit tests.

## Recommended Structure
```text
my-crate/
├── my-crate/            # Main runtime crate
├── my-crate-derive/     # proc-macro = true shim (just parses and forwards)
└── my-crate-internal/   # Normal library with syn/quote and full unit tests
```

## Good
```rust
// In my-crate-derive/src/lib.rs (thin proc-macro shim)
#[proc_macro_derive(MyTrait)]
pub fn derive_my_trait(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
    let input = syn::parse_macro_input!(input as syn::DeriveInput);
    my_crate_internal::expand_derive(input)
        .unwrap_or_else(syn::Error::into_compile_error)
        .into()
}
```
