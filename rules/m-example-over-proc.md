# m-example-over-proc

> Prefer declarative `macro_rules!` (macros by example) over procedural macros when possible.

## Why It Matters
Procedural macros require compiling a separate dylib host crate with heavy dependencies (`syn`, `quote`, `proc-macro2`), significantly increasing clean build times. `macro_rules!` compiles instantly inside the same crate.

## Bad
```rust
// Proc-macro derive crate pulled in just for basic boilerplate repetition
#[derive(MyTrivialDerive)]
struct Point { x: i32, y: i32 }
```

## Good
```rust
// Zero additional dependencies, instant compilation
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
