# m-errors-canonical

> Library errors must be typed and inspectable; use `thiserror` when it fits the crate.

## Why It Matters
Returning only `String`, `Box<dyn Error>`, or `anyhow::Error` from library code prevents callers from reliably inspecting, matching, or recovering from specific error cases. A typed enum, struct, or newtype is appropriate; `thiserror` is a convenient implementation when compatible with the crate's goals, including `no_std` constraints.

## Bad
```rust
// Downstream consumers cannot match or inspect error causes
pub fn read_config(path: &Path) -> Result<Config, Box<dyn std::error::Error>> {
    ...
}
```

## Good
```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("failed to read configuration file: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("invalid syntax on line {line}: {msg}")]
    Syntax { line: usize, msg: String },
    
    #[error("required key '{0}' is missing")]
    MissingKey(String),
}

pub fn read_config(path: &Path) -> Result<Config, ConfigError> {
    ...
}
```

## When Acceptable
Use `anyhow` or `eyre` in final application binaries (CLI, web services, GUI) where errors are only printed to the user/logs.
