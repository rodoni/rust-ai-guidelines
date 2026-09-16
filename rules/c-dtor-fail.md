# c-dtor-fail

> Destructors (`Drop` trait implementations) must never panic or fail.

## Why It Matters
When a thread panics and unwinds the stack, destructors of all stack-allocated variables are executed. If a destructor panics during unwinding, Rust has no choice but to immediately abort the entire process (`SIGABRT`). Destructors must silently absorb or log cleanup errors.

## Bad
```rust
pub struct TempFile {
    path: std::path::PathBuf,
}

impl Drop for TempFile {
    fn drop(&mut self) {
        // Will panic if file does not exist or permissions fail!
        std::fs::remove_file(&self.path).unwrap(); // Dangerous abort!
    }
}
```

## Good
```rust
pub struct TempFile {
    path: std::path::PathBuf,
}

impl Drop for TempFile {
    fn drop(&mut self) {
        // Ignore or log error without panicking
        if let Err(err) = std::fs::remove_file(&self.path) {
            // In libraries/services: use telemetry without panic
            let _ = err;
        }
    }
}
```

## See Also
- [m-panic-on-bug](m-panic-on-bug.md) - Panics are strictly for unrecoverable bugs
- [m-log-not-print](m-log-not-print.md) - Production code uses telemetry
