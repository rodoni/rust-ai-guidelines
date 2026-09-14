# c-common-traits

> Eagerly implement or derive standard library traits on public types.

## Why It Matters
Types lacking basic traits (`Debug`, `Clone`, `Default`, `PartialEq`, `Eq`, `Hash`) cannot be inspected, collected, or easily integrated by downstream consumers, causing friction.

## Standard Traits Checklist
- **`Debug`**: Mandatory on virtually all public types.
- **`Clone`**: On types where cloning has a sensible implementation.
- **`Default`**: On types with an obvious empty or neutral state.
- **`PartialEq`, `Eq`, `Hash`**: On identifier or value-like types.

## Bad
```rust
// Downstream consumers cannot debug, clone or store this in a HashSet
pub struct RequestId {
    raw: uuid::Uuid,
}
```

## Good
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default)]
pub struct RequestId {
    raw: uuid::Uuid,
}
```

## When Acceptable
Do not derive `Copy` or `Clone` if the type represents an exclusive resource (e.g. file lock, single-use token).
