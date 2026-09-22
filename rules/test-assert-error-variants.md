# test-assert-error-variants

> Assert specific error enum variants with `matches!` or `assert_matches!`, never just `.is_err()`.

## Why It Matters
Asserting only `assert!(result.is_err())` creates false-positive test passes. The function might fail for an entirely unrelated reason (such as an invalid authorization token, unparseable payload, or missing file) rather than the specific condition being tested (such as duplicate key rejection). Checking the explicit error variant ensures API contracts and failure branches remain sound.

## Bad
```rust
#[test]
fn test_user_duplicate_rejected() {
    let mut repo = UserRepo::default();
    repo.insert("alice@example.com").unwrap();

    let result = repo.insert("alice@example.com");
    // BAD: Passes if insert fails for ANY reason (e.g. database timeout or invalid email syntax)!
    assert!(result.is_err());
}
```

## Good
```rust
#[test]
fn test_user_duplicate_rejected() {
    let mut repo = UserRepo::default();
    repo.insert("alice@example.com").unwrap();

    let result = repo.insert("alice@example.com");
    // GOOD: Explicitly verifies the domain invariant and error variant
    assert!(
        matches!(result, Err(UserError::DuplicateEmail(ref email)) if email == "alice@example.com"),
        "expected DuplicateEmail error, got: {result:?}"
    );
}
```

## When Acceptable
Coarse-grained sanity checks on opaque errors (e.g. top-level CLI handlers returning `anyhow::Result<()>`) where internal error variants are deliberately erased.
