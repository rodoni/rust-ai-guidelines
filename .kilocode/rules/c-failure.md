# c-failure

> Public API documentation must contain explicit `# Errors`, `# Panics`, and `# Safety` sections.

## Why It Matters
Contractual expectations must be clear. Missing `# Panics` or `# Safety` sections causes callers and AI coding agents to make incorrect assumptions regarding error handling or preconditions.

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
/// Panics if `path` is an empty string.
///
/// # Safety
/// (If unsafe fn) Specifies caller-upheld memory preconditions.
pub fn read_int(path: &Path) -> Result<i32, IoError> { ... }
```
