# m-ffi-translates

> FFI crates must only translate types and calls; business logic belongs in pure Rust core crates.

## Why It Matters
Mixing business logic into C-ABI FFI wrapper functions prevents code reuse by native Rust consumers, hinders unit testing, and complicates memory boundary management.

## Bad
```rust
// Business logic coupled directly to raw C-ABI pointers
#[no_mangle]
pub unsafe extern "C" fn calculate_score_ffi(data_ptr: *const u8, len: usize) -> f64 {
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
#[no_mangle]
pub unsafe extern "C" fn calculate_score_ffi(data_ptr: *const u8, len: usize, out: *mut f64) -> i32 {
    if data_ptr.is_null() || out.is_null() {
        return -1; // Status code error
    }
    // SAFETY: caller guarantees non-null and valid slice length
    let slice = unsafe { std::slice::from_raw_parts(data_ptr, len) };
    match calculate_score(slice) {
        Ok(score) => {
            unsafe { *out = score };
            0 // Success
        }
        Err(_) => -2,
    }
}
```
