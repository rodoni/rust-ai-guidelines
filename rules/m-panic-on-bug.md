# m-panic-on-bug

> Panics are exclusively for impossible invariants and programming bugs; use `Result` for runtime failures.

## Why It Matters
Panics may unwind the current thread or abort the process when configured to do so. Crates that panic on bad network packets, invalid user inputs, or disk failures make client applications unreliable and prone to denial-of-service.

## Bad
```rust
// Panicking on invalid user/network input
pub fn parse_header(line: &str) -> Header {
    let parts: Vec<&str> = line.split(':').collect();
    if parts.len() < 2 {
        panic!("Invalid header format!"); // NEVER do this
    }
    Header { key: parts[0].into(), val: parts[1].into() }
}
```

## Good
```rust
// Return Result for recoverable expected runtime conditions
pub fn parse_header(line: &str) -> Result<Header, ParseError> {
    let (key, val) = line.split_once(':').ok_or(ParseError::MissingColon)?;
    Ok(Header { key: key.trim().into(), val: val.trim().into() })
}

// Panic/assert only for unreachable internal state (programming bug)
fn internal_state_step(&mut self) {
    assert!(self.initialized, "internal bug: step called before init");
}
```
