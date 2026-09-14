# m-unsound-prevention

> Public safe APIs wrapping `unsafe` internals must be 100% sound under all possible inputs.

## Why It Matters
If a public safe function can trigger undefined behavior (UB) with any safe inputs or calling patterns, the crate is unsound. Safe code must never be able to cause memory corruption or UB.

## Bad
```rust
pub struct SafeSlice<'a> {
    ptr: *const u8,
    len: usize,
    _marker: std::marker::PhantomData<&'a u8>,
}

impl<'a> SafeSlice<'a> {
    // Safe function allowing caller to pass arbitrary invalid pointers: UNSOUND!
    pub fn new(ptr: *const u8, len: usize) -> Self {
        SafeSlice { ptr, len, _marker: std::marker::PhantomData }
    }
}
```

## Good
```rust
impl<'a> SafeSlice<'a> {
    // Marked `unsafe fn` because caller must uphold pointer validity invariants
    /// # Safety
    /// `ptr` must be non-null, aligned, and point to `len` initialized bytes.
    pub unsafe fn from_raw_parts(ptr: *const u8, len: usize) -> Self {
        SafeSlice { ptr, len, _marker: std::marker::PhantomData }
    }
    
    // Safe constructor takes safe Rust reference
    pub fn from_slice(slice: &'a [u8]) -> Self {
        SafeSlice {
            ptr: slice.as_ptr(),
            len: slice.len(),
            _marker: std::marker::PhantomData,
        }
    }
}
```
