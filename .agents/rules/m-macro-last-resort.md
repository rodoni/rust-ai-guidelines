# m-macro-last-resort

> Treat macros as a tool of last resort; prefer functions, traits, and generics.

## Why It Matters
Macros obscure compiler diagnostics, bloat compile times, complicate IDE autocomplete and code navigation, and can hide subtle hygiene and syntax bugs.

## Decision Matrix
1. Can it be a function? Use a function.
2. Can it be a generic function or trait? Use generics/traits.
3. Does it require syntactic pattern generation or compile-time AST inspection? Only then use a macro.

## Bad
```rust
// Macro used where a simple generic function works perfectly
macro_rules! add {
    ($a:expr, $b:expr) => {
        $a + $b
    };
}
```

## Good
```rust
#[inline]
pub fn add<T: std::ops::Add<Output = T>>(a: T, b: T) -> T {
    a + b
}
```
