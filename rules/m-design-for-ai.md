# m-design-for-ai

> Design APIs and modules for AI comprehension: idiomatic patterns, strong types, and testable examples.

## Why It Matters
AI coding agents excel when code follows established idioms and strict type invariants. Obscure abstractions, primitive obsession, and missing doc contracts increase hallucinations and subtle logical bugs.

## Bad
```rust
// Primitive obsession and missing documentation lead AI to swap arguments
pub fn enqueue_item(&mut self, user_id: u64, org_id: u64, payload: &[u8]) -> bool {
    // Unclear failure mode, easy for LLM to swap user_id and org_id
    true
}
```

## Good
```rust
/// Enqueues a transaction for processing.
///
/// # Errors
/// Returns `QueueError::Full` if the internal ring buffer is saturated.
///
/// # Examples
/// ```
/// # use my_crate::{Queue, TransactionId, UserId};
/// # fn run(queue: &mut Queue, u: UserId, tx: TransactionId) -> Result<(), Box<dyn std::error::Error>> {
/// queue.enqueue(u, tx)?;
/// # Ok(())
/// # }
/// ```
pub fn enqueue(&mut self, user: UserId, tx: TransactionId) -> Result<(), QueueError> {
    // Strong Newtypes prevent swapped arguments
    Ok(())
}
```

## See Also
- [c-newtype](c-newtype.md) - Use Newtypes for domain identifiers
- [c-failure](c-failure.md) - Mandatory doc failure sections
