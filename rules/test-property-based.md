# test-property-based

> Use property-based testing (`proptest`) for pure functions, parsers, serialization, and domain invariants.

## Why It Matters
Example-based tests only verify hand-picked data points that conform to human (or LLM) bias, easily missing integer overflow, empty collections, malformed UTF-8, and unexpected edge states. Property-based tests generate hundreds of pseudo-random inputs and automatically shrink failing cases to the minimal reproducible counterexample.

## Bad
```rust
// Only tests two arbitrary happy-path cases; misses overflows and roundtrip bugs
#[test]
fn test_roundtrip() {
    let original = "hello";
    let encoded = encode(original);
    assert_eq!(decode(&encoded).unwrap(), original);
}
```

## Good
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_encode_decode_roundtrip(s in "\\PC*") {
        let encoded = encode(&s);
        let decoded = decode(&encoded).expect("valid input must decode");
        prop_assert_eq!(decoded, s);
    }

    #[test]
    fn test_numeric_invariant(a in 0u32..10_000, b in 1u32..10_000) {
        let result = safe_divide_scale(a, b);
        prop_assert!(result <= a);
    }
}
```

## When Acceptable
High-level integration tests hitting real databases or slow network I/O where running hundreds of iterations per test is prohibitively slow; use standard unit tests with targeted fixtures instead.
