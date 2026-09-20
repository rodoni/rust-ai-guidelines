# wf-atomic-steps

> Execute changes in small, testable, and reversible steps, keeping the workspace compilable at every step.

## Why It Matters
Simultaneously modifying multiple structs, traits, and call sites across a workspace produces overwhelming compiler diagnostic output. When 40 errors appear at once, reasoning breaks down and agents hallucinate circular fixes. Making single, atomic modifications verified by `cargo check` isolates regressions immediately.

## Bad
```bash
# Modifying 8 crates and 15 files in a single pass without intermediate checks
# Result: 52 compiler errors, broken dependencies, impossible to isolate root cause
```

## Good
```bash
# Step 1: Add new trait or method signature with #[allow(dead_code)]
cargo check --workspace

# Step 2: Implement trait for one concrete struct; write unit test
cargo test -p my-crate --lib test_trait_impl

# Step 3: Migrate call sites incrementally, one file at a time
cargo check --workspace

# Step 4: Remove deprecated code and verify lints
cargo clippy --workspace -- -D warnings
```

## When Acceptable
Initial greenfield workspace scaffolding where crates are being established and no inter-crate dependencies have been linked yet.
