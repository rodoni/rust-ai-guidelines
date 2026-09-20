# m-test-util

> Gate test fixtures, fakes, and harness utilities behind `feature = "test-util"`.

## Why It Matters
Downstream crates and integration tests frequently need mock drivers or test fixtures. Putting them in `tests/` prevents other crates from reusing them; putting them in `src/` without feature flags exposes test-only API and dependencies to normal builds and can increase compile or release costs.

## Bad
```rust
// Unconditionally compiled into production release binaries!
pub struct FakeDatabaseClient { ... }
```

## Good
```rust
// In Cargo.toml:
// [features]
// test-util = []

#[cfg(feature = "test-util")]
pub struct FakeDatabaseClient {
    pub records: std::sync::Mutex<Vec<Record>>,
}
```
