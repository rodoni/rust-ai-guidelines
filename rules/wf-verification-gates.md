# wf-verification-gates

> Pass all deterministic verification gates (`cargo fmt`, `cargo check`, `cargo clippy`, `cargo test`) before declaring a task complete.

## Why It Matters
AI agents often declare success based on intuitive reasoning while missing subtle type mismatches, unused imports, lint warnings, or broken tests. Enforcing an unskippable deterministic verification pipeline provides mathematical proof of correctness and ensures zero regressions enter the codebase.

## Bad
```markdown
"I have updated the lock manager implementation. The changes look correct and handle all edge cases."
(Did not execute `cargo check` or `cargo test`; the code actually fails to compile due to a missing `Send` bound!)
```

## Good
```bash
# Gate 1: Syntax & Formatting
cargo fmt --all -- --check

# Gate 2: Compilation & Types
cargo check --all-targets --workspace

# Gate 3: Lints & Idioms (Zero Warnings Tolerance)
cargo clippy --all-targets --workspace -- -D warnings

# Gate 4: Test Suite & Doc Tests
cargo test --workspace --all-features
```

## When Acceptable
When working in environments without local Cargo toolchain access, or when drafting preliminary architectural documents that do not alter Rust source files.
