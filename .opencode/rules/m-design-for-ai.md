# m-design-for-ai

> Design APIs and modules for AI comprehension: idiomatic patterns, strong types, and testable examples.

## Why It Matters
AI coding agents excel when code follows established idioms and strict type invariants. Obscure abstractions, primitive obsession, and missing doc contracts increase hallucinations and subtle logical bugs.

## Key Principles for AI-Friendly Rust
1. **Strong Newtypes**: Use distinct types (`UserId(u64)`) rather than raw primitives (`u64`) so the compiler catches AI mixups immediately.
2. **Explicit Doc Contracts**: Provide complete `# Errors` and `# Panics` sections.
3. **Copy-Pastable Doc Examples**: Write runnable doc examples using `?` rather than `unwrap()` or hidden boilerplate.
4. **Standard Ecosystem Patterns**: Conform to standard `std` and `tokio` idioms instead of inventing bespoke custom control flow.

## Good
```rust
/// Enqueues a transaction for processing.
///
/// # Examples
/// ```
/// # use my_crate::{Queue, TransactionId};
/// # fn run(queue: &mut Queue, tx_id: TransactionId) -> Result<(), Box<dyn std::error::Error>> {
/// queue.enqueue(tx_id)?;
/// # Ok(())
/// # }
/// ```
pub fn enqueue(&mut self, id: TransactionId) -> Result<(), QueueError> { ... }
```
