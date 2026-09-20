# m-app-error

> Use `anyhow` for top-level application error handling; public reusable libraries should expose typed errors.

## Why It Matters
Applications need rich context chains, backtraces, and convenient error reporting to humans and logs, whereas public libraries should provide typed, inspectable errors that callers can match on. Internal crates belonging only to one application may reasonably share the application's error strategy.

## Bad
```rust
// In a library crate (breaks downstream matching)
pub fn parse_data(raw: &str) -> anyhow::Result<Data> { ... }
```

## Good
```rust
// 1. In a public library crate: typed, inspectable error
pub fn parse_data(raw: &str) -> Result<Data, ParseError> { ... }

// 2. In application binary (main.rs / CLI / Server):
use anyhow::Context;

fn main() -> anyhow::Result<()> {
    let config = read_config(&path)
        .with_context(|| format!("Failed to read config from {:?}", path))?;
    Ok(())
}
```
