# m-log-not-print

> Use structured telemetry for service diagnostics; reserve direct stdout/stderr for deliberate presentation output.

## Why It Matters
`println!`, `eprintln!`, and `dbg!` bypass log filtering and structured fields when used for diagnostics. They are appropriate in a CLI presentation layer only when the output is intentional, documented, and separate from service telemetry.

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
