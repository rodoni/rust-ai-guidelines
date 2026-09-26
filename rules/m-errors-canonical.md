# m-errors-canonical

> Library errors should be situation-specific structs with captured backtraces and query methods; avoid leaking error enums.

## Why It Matters
Exposing large public error enums in library crates leaks internal failure modes and tightly couples consumers to private implementation details. A situation-specific error `struct` containing a `Backtrace` and semantic query methods (`is_syntax_error()`, `is_io()`) encapsulates the error topology while allowing internal variants (`ErrorKind`) to evolve without breaking semver (Microsoft Pragmatic Rust `M-ERRORS-CANONICAL-STRUCTS`).

## Bad
```rust
// Large public enum exposing internal dependency errors directly:
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error), // Leaks std::io directly into public contract!
    #[error("Syntax error at line {0}")]
    Syntax(usize),
}
```

## Good
```rust
use std::backtrace::Backtrace;
use std::path::Path;

#[derive(Debug)]
pub(crate) enum ErrorKind {
    Io(std::io::Error),
    Syntax { line: usize },
}

#[derive(Debug)]
pub struct ConfigError {
    kind: ErrorKind,
    backtrace: Backtrace,
}

impl ConfigError {
    pub(crate) fn new(kind: ErrorKind) -> Self {
        Self {
            kind,
            backtrace: Backtrace::capture(),
        }
    }

    /// Semantic query method: allows handling without exposing raw error variants.
    pub fn is_syntax_error(&self) -> bool {
        matches!(self.kind, ErrorKind::Syntax { .. })
    }

    pub fn is_io(&self) -> bool {
        matches!(self.kind, ErrorKind::Io(_))
    }
}
```

## When Acceptable
Application binaries (CLI, servers) should use `anyhow` ([m-app-error](m-app-error.md)). Simple internal crates with closed failure domains may use private or local enums when future-proofing against semver breakage is not required.

## See Also
- [m-app-error](m-app-error.md) - Use anyhow in applications, typed errors in libraries
- [m-dont-leak-types](m-dont-leak-types.md) - Do not leak internal foreign crate types
