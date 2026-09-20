# wf-tdd-loop

> Write reproducible tests that fail first before implementing new features or bug fixes (Red-Green-Refactor).

## Why It Matters
Writing tests after the implementation often results in superficial assertions that test what the code *does*, rather than what it *must do*. Starting with a failing test pins down exact requirements, edge cases, and regression scenarios. In Rust, a compile-time failure or runtime test assertion serves as a definitive validation milestone.

## Bad
```rust
// Modifying business logic directly without an existing failing test
pub fn compute_discount(price: u64, tier: UserTier) -> u64 {
    // "Fixed bug where VIPs were charged full price"
    // No test was written to prove the bug existed or that other tiers remain unaffected!
}
```

## Good
```rust
// Step 1 (RED): Write test reproducing the bug or feature specification
#[test]
fn vip_receives_twenty_percent_discount() {
    let price = 100;
    let final_price = compute_discount(price, UserTier::Vip);
    assert_eq!(final_price, 80); // Fails initially: asserts bug existence
}

// Step 2 (GREEN): Write minimal code to satisfy the test
pub fn compute_discount(price: u64, tier: UserTier) -> u64 {
    match tier {
        UserTier::Vip => price * 80 / 100,
        UserTier::Standard => price,
    }
}

// Step 3 (REFACTOR): Optimize memory and structure while keeping tests green
```

## When Acceptable
Pure data definitions (structs/enums without behavior), initial prototype exploration where requirements are completely unformed, or auto-generated boilerplate.
