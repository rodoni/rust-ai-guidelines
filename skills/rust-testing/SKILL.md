---
name: rust-testing
description: >
  Comprehensive guidelines for writing high-confidence, idiomatic Rust unit, integration,
  property-based, and async tests with minimal maintenance overhead and zero token waste.
---

# Rust Testing & Verification Guidelines

Engineering standards for robust, deterministic, and maintainable test suites in Rust. Enforces high-leverage testing patterns: property-based testing, in-memory fakes, precise error assertions, deterministic time simulation, and snapshot testing.

## Rules Index

| Rule | Impact | Summary |
|---|---|---|
| [`test-property-based`](../../rules/test-property-based.md) | HIGH | Use property-based testing (`proptest`) for pure logic, codecs, and invariants. |
| [`test-assert-error-variants`](../../rules/test-assert-error-variants.md) | HIGH | Assert specific error enum variants with `matches!`, never just `.is_err()`. |
| [`test-deterministic-no-sleep`](../../rules/test-deterministic-no-sleep.md) | HIGH | Eliminate wall-clock `sleep`; use simulated time or `tokio::time::pause()`. |
| [`test-fakes-over-heavy-mocks`](../../rules/test-fakes-over-heavy-mocks.md) | MEDIUM | Prefer simple in-memory fakes over complex dynamic mocking frameworks. |
| [`test-behavior-not-internals`](../../rules/test-behavior-not-internals.md) | HIGH | Test observable module contracts and invariants, not ephemeral private helpers. |
| [`test-snapshot-for-complex-data`](../../rules/test-snapshot-for-complex-data.md) | MEDIUM | Use snapshot testing (`insta`) for large structs, ASTs, and CLI output. |
| [`wf-tdd-loop`](../../rules/wf-tdd-loop.md) | CRITICAL | Write reproducible failing tests before implementing features or bug fixes. |
| [`wf-verification-gates`](../../rules/wf-verification-gates.md) | CRITICAL | Validate changes against `cargo fmt`, `check`, `clippy`, and `test`. |
| [`m-test-util`](../../rules/m-test-util.md) | MEDIUM | Gate test fixtures and fakes behind `feature = "test-util"`. |
| [`m-mockable-syscalls`](../../rules/m-mockable-syscalls.md) | HIGH | Design core domain logic "sans I/O" or behind mockable traits. |

---

## 🎯 Testing Hierarchy in Rust

1. **Unit Tests (`src/**/tests.rs` or `mod tests`)**:
   - Reside alongside the implementation inside `#[cfg(test)] mod tests { use super::*; ... }`.
   - Verify specific component invariants and logic boundaries.
   - Fast, in-memory, zero network/disk access.
2. **Integration Tests (`tests/*.rs`)**:
   - Independent crates exercising only public APIs (`pub`).
   - Validate realistic end-to-end multi-component workflows.
   - Use shared test helpers from `tests/common/mod.rs` or a `test-util` feature.
3. **Documentation Tests (Doc-tests in `/// ```rust`)**:
   - Validated automatically by `cargo test`.
   - Ensure public API examples remain runnable, correct, and up-to-date with compiler checks.
