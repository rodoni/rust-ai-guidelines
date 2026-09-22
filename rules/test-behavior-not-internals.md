# test-behavior-not-internals

> Test observable module behavior and domain invariants, not private volatile implementation details.

## Why It Matters
Unit tests tightly coupled to ephemeral private functions or internal layout details become brittle. They break upon harmless internal refactoring even when the component's public contract and domain invariants remain fully satisfied. Testing at the interface boundary ensures tests serve as durable safety nets rather than refactoring anchors.

## Bad
```rust
// Coupling tests directly to private helper steps
#[test]
fn test_private_hash_step() {
    let hasher = TokenGenerator::default();
    // Testing private transient helper: breaks immediately if algorithm changes internally
    let intermediate = hasher.compute_step_a_nonce(b"seed");
    assert_eq!(intermediate, 0xcafe);
}
```

## Good
```rust
// Testing observable contract and output invariants
#[test]
fn test_token_generator_contract() {
    let generator = TokenGenerator::default();
    let token = generator.generate_token(b"seed").expect("token generation must succeed");

    // Asserts public invariants: length, entropy, and non-emptiness
    assert_eq!(token.len(), 32);
    assert!(token.is_valid_format());
}
```

## When Acceptable
Isolated mathematical or cryptographic kernels (such as specialized numerical algorithms, bit-twiddling primitives, or custom hash rounds) where separate unit verification of the raw internal primitive is essential.
