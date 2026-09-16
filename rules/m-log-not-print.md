# m-log-not-print

> Production code uses structured telemetry (`tracing`/`log`), never `println!`, `eprintln!`, or `dbg!`.

## Why It Matters
`println!` and `dbg!` write unbuffered or uncoordinated text directly to standard output/error, bypass log filtering levels, cannot be ingested by structured telemetry systems, and ruin CLI applications that pipe binary or JSON output.

## Bad
```rust
pub async fn process_payment(order_id: u64, amount: u64) {
    // Uncoordinated stdout output in production!
    println!("Processing order: {} with amount: {}", order_id, amount);
    dbg!(order_id);
}
```

## Good
```rust
use tracing::{info, instrument};

#[instrument(skip(amount))]
pub async fn process_payment(order_id: u64, amount: u64) {
    // Structured, filterable telemetry
    info!(order_id, amount, "Processing payment");
}
```

## See Also
- [m-log-structured](m-log-structured.md) - Structured key-value telemetry
- [m-mockable-syscalls](m-mockable-syscalls.md) - Mockable system dependencies
