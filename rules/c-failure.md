# c-failure

> Document fallibility and safety contracts explicitly in public APIs.

## Why It Matters
Contractual expectations must be clear. Add `# Errors` when an API returns a recoverable error, `# Panics` when it can panic, and `# Safety` only for `unsafe` APIs.

## Bad
```rust
/// Reads an integer from file.
pub fn read_int(path: &Path) -> Result<i32, IoError> { ... }
```

## Good
```rust
/// Reads a 32-bit integer from the specified file.
///
/// # Errors
/// Returns an [`std::io::Error`] if the file does not exist, permission is denied,
/// or the file contains fewer than 4 bytes.
///
/// # Panics
/// Never panics for valid `Path` values.
pub fn read_int(path: &Path) -> Result<i32, IoError> { ... }
```
