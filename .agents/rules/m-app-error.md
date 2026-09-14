# m-app-error

> Use `anyhow` for top-level application binary error handling, but never in library crates.

## Why It Matters
Applications need rich context chains, backtraces, and convenient error reporting to humans and logs, whereas libraries must provide structured enum types that callers can match on.

## Bad
```rust
// In a library crate (breaks downstream matching)
pub fn parse_data(raw: &str) -> anyhow::Result<Data> { ... }
```

## Good
```rust
// 1. In library crate: strongly typed enum
pub fn parse_data(raw: &str) -> Result<Data, ParseError> { ... }

// 2. In application binary (main.rs / CLI / Server):
use anyhow::Context;

fn main() -> anyhow::Result<()> {
    let config = read_config(&path)
        .with_context(|| format!("Failed to read config from {:?}", path))?;
    Ok(())
}
```
