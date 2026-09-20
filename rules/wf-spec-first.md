# wf-spec-first

> Define and align types, traits, contracts, and invariants before writing executable implementation code.

## Why It Matters
Jumping straight into editing function bodies in Rust leads to cascading *borrow checker* failures and lifetime mismatches across multiple files. Designing the type system, traits, error enums, and ownership boundaries first ensures all components align with Rust's strict compiler guarantees before investing effort in logic.

## Bad
```rust
// Modifying implementation before agreeing on signatures and contracts
pub fn parse_and_store(raw_data: &[u8]) {
    // 50 lines of complex parsing logic using ad-hoc tuples and unwraps
    // Later discovers this violates thread safety (cannot cross Tokio task boundary)
    // Entire implementation must be discarded and rewritten!
}
```

## Good
```rust
// Step 1: Spec-First - Define domain types, errors, and trait contracts
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MeasurementId(pub u64);

#[derive(thiserror::Error, Debug)]
pub enum TelemetryError {
    #[error("payload malformed at offset {0}")]
    Malformed(usize),
}

pub trait TelemetrySink: Send + Sync {
    fn record(&self, id: MeasurementId, val: f64) -> Result<(), TelemetryError>;
}

// Step 2: Implementation proceeds only after the contract is proven sound
```

## When Acceptable
Trivial single-line changes, fixing typos in docstrings, or local variable renaming within an already validated function.
