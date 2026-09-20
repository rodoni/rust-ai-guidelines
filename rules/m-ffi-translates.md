# m-ffi-translates

> FFI crates must only translate types and calls; business logic belongs in pure Rust core crates.

## Why It Matters
Mixing business logic into C-ABI FFI wrapper functions prevents code reuse by native Rust consumers, hinders unit testing, and complicates memory boundary management.

## Bad
```rust
// Business logic coupled directly to raw C-ABI pointers
#[no_mangle]
pub unsafe extern "C" fn mycrate_score_calculate(data_ptr: *const u8, len: usize) -> f64 {
    // 50 lines of complex parsing and mathematical calculations...
}
```

## Good
```rust
// 1. In core pure-Rust crate (easy to test, idiomatically typed)
pub fn calculate_score(data: &[u8]) -> Result<f64, ScoreError> {
    // Pure logic
}

// 2. In *-sys or *-ffi crate (purely mechanical translation)
/// # Safety
/// `data_ptr` must be non-null, aligned for `u8`, and point to `len` initialized
/// bytes readable for the duration of this call. `out` must be non-null, aligned
/// for `f64`, and uniquely writable for the duration of this call.
#[no_mangle]
pub unsafe extern "C" fn mycrate_score_calculate(data_ptr: *const u8, len: usize, out: *mut f64) -> i32 {
    if data_ptr.is_null() || out.is_null() {
        return -1; // Status code error
    }
    // SAFETY: the function contract requires a valid, aligned, initialized
    // `len`-byte read from `data_ptr` for the duration of this call.
    let slice = unsafe { std::slice::from_raw_parts(data_ptr, len) };
    match calculate_score(slice) {
        Ok(score) => {
            // SAFETY: the function contract requires `out` to be aligned,
            // uniquely writable, and valid for one initialized `f64` write.
            unsafe { *out = score };
            0 // Success
        }
        Err(_) => -2,
    }
}
```
