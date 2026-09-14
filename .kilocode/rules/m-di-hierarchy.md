# m-di-hierarchy

> Prefer concrete types over generics, and generics over `dyn Trait`.

## Why It Matters
Over-abstracting with `dyn Trait` causes virtual dispatch, breaks inlining, and prevents compiler optimizations. Premature generics increase compile times and complicate signatures.

## Hierarchy Rule
1. **Concrete types**: Simplest, fastest compilation, easiest for AI and humans to understand.
2. **Generics with bounds (`impl Trait`)**: When genuine polymorphism is needed with zero runtime cost.
3. **Trait Objects (`dyn Trait`)**: Only when heterogeneous collections or dynamic plugins are strictly necessary.

## Bad
```rust
// Unnecessary dynamic dispatch and allocation
pub fn write_log(writer: &mut Box<dyn std::io::Write>, msg: &str) {
    let _ = writeln!(writer, "{msg}");
}
```

## Good
```rust
// Generic with trait bound: monomorphized, inlined, zero-cost
pub fn write_log(mut writer: impl std::io::Write, msg: &str) {
    let _ = writeln!(writer, "{msg}");
}
```
