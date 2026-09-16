# c-smart-ptr

> Smart pointers do not add inherent methods to avoid method resolution collisions with dereferenced targets.

## Why It Matters
When calling `ptr.foo()`, Rust auto-dereferences `ptr` to look for `.foo()` on the target type. If the smart pointer defines its own inherent methods (like `.clone()` or `.len()`), it shadows the target type's methods, causing confusing compiler errors or silent semantic bugs.

## Bad
```rust
pub struct MyBox<T>(Box<T>);

impl<T> MyBox<T> {
    // Inherent method shadows target's .len() if T is Vec or str!
    pub fn len(&self) -> usize {
        1
    }
}
```

## Good
```rust
pub struct MyBox<T>(Box<T>);

// If smart pointer needs metadata or utility operations,
// expose them as static associated functions, not methods with `&self`
impl<T> MyBox<T> {
    pub fn new(val: T) -> Self {
        Self(Box::new(val))
    }

    pub fn into_inner(this: Self) -> T {
        *this.0
    }
}
```

## See Also
- [c-deref](c-deref.md) - Only smart pointers implement Deref
- [m-avoid-wrappers](m-avoid-wrappers.md) - Avoid smart pointers in public signatures
