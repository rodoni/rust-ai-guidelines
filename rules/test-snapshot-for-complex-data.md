# test-snapshot-for-complex-data

> Use snapshot testing (`insta`) for complex nested data structures, ASTs, compiler diagnostics, and CLI outputs.

## Why It Matters
Manually handcrafting dozens of nested field assertions (`assert_eq!(ast.body[0].kind, ...)`) creates immense maintenance overhead, obfuscates test intent, and makes reviewing changes painful. Snapshot testing captures the serialized structural output into reviewable files, turning regressions into readable diffs.

## Bad
```rust
#[test]
fn test_parse_query() {
    let query = parse_sql("SELECT id, name FROM users WHERE active = true").unwrap();
    // Brittle, verbose manual inspection of deep nested fields
    assert_eq!(query.projections.len(), 2);
    assert_eq!(query.projections[0].as_col(), "id");
    assert_eq!(query.projections[1].as_col(), "name");
    assert!(query.filter.is_some());
    // 30 more lines verifying every sub-expression...
}
```

## Good
```rust
#[test]
fn test_parse_query() {
    let query = parse_sql("SELECT id, name FROM users WHERE active = true").unwrap();

    // Concise, auditable snapshot captures full semantic structure
    insta::assert_yaml_snapshot!(query);
}
```

## When Acceptable
Simple scalar values, single error codes, numeric calculations, or small structures where a single `assert_eq!` is immediately obvious and does not generate noisy snapshot churn.
