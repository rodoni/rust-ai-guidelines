# m-regular-fn

> Prefer regular standalone functions over empty dummy structs with associated functions.

## Why It Matters
Creating empty dummy structs just to namespace functions (e.g. `MathUtils::calculate()`) is an object-oriented Java/C# antipattern. Rust uses modules (`math_utils::calculate()`) for namespacing.

## Bad
```rust
// Unidiomatic OOP-style utility class
pub struct StringHelper;

impl StringHelper {
    pub fn sanitize(input: &str) -> String { ... }
}
```

## Good
```rust
// Idiomatic module-level functions
pub mod string_utils {
    pub fn sanitize(input: &str) -> String { ... }
}
```
