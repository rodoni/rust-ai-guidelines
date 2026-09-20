# m-example-over-proc

> Prefer declarative `macro_rules!` (macros by example) over procedural macros when possible.

## Why It Matters
Procedural macros require compiling a separate host crate and often bring dependencies such as `syn`, `quote`, and `proc-macro2`, which can increase clean build times. `macro_rules!` avoids that separate proc-macro crate, although its expansion still has compilation cost.

## Bad
```rust
// Proc-macro derive crate pulled in just for basic boilerplate repetition
#[derive(MyTrivialDerive)]
struct Point { x: i32, y: i32 }
```

## Good
```rust
// No separate proc-macro crate is needed
macro_rules! impl_point {
    ($t:ident) => {
        impl $t {
            pub fn origin() -> Self { Self { x: 0, y: 0 } }
        }
    };
}

impl_point!(Point);
```

## When Acceptable
Use procedural derive macros when inspecting complex struct fields, parsing custom attributes, or doing non-trivial compile-time code synthesis.
