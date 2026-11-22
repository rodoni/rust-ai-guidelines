# Fixed Tasks and Scoring Key

Use the exact prompt text in each task for both conditions. The scorer should
use the criteria and answer key below only after outputs are anonymized. Do not
show the answer-key sections to the model.

Each task starts from a fresh `fixture/initial` reset. The runner applies the
specified mutant to reviewer tasks and TEST-2 after reset; the same mutant is
used in every run. Reviewer changes are review targets, not instructions to fix
them.

## DEV-1: checked mean

**Persona:** `rust-dev`
**Prompt:** “Implement `checked_mean(values: &[i32]) -> Option<f64>` in `src/lib.rs`. Return `None` for an empty slice. For non-empty input, return the arithmetic mean without overflowing for any possible slice length and i32 values. Add behavior tests for empty input, positive and negative fractional means, and an input whose i32 sum overflows. Do not change `mean`.”

**Expected:** New function leaves `mean` unchanged; accumulation must not overflow for any addressable `&[i32]` on supported 32/64-bit Rust targets. An `i128` accumulator is sufficient for the maximum slice byte length; `i64` alone is not sufficient for every theoretically addressable 64-bit slice. A floating-point approach avoids integer overflow but must return a reasonable `f64` mean. Empty returns `None`; fractional result is correct; tests cover all stated cases.

**Score 0–4:** 1 point each for unchanged existing API, correct empty/fractional behavior, an accumulator strategy that cannot overflow for an addressable slice, and meaningful tests covering all requested cases. 0 if it does not compile. An `i64` accumulator loses the no-overflow point because a 64-bit slice can exceed `i64::MAX` when summed.

## DEV-2: first maximum bug

**Persona:** `rust-dev`
**Prompt:** “Fix `first_max_index` in `src/lib.rs`. It must return the index of the first occurrence of the largest value, or `None` for an empty slice. Add a regression test demonstrating the bug with repeated maxima, plus empty and singleton boundary tests. Keep the public signature unchanged.”

**Expected:** Replace `>=` with `>` or equivalent logic that preserves the first maximum; regression test distinguishes `[4, 9, 9, 2]` (expected `Some(1)`); empty and singleton covered; signature unchanged.

**Score 0–4:** 1 point each for correct repeated-maximum result, empty handling, singleton handling, and focused regression/boundary tests. 0 if it does not compile.

## REV-1: overflow contract

**Persona:** `rust-reviewer`
**Proposed change:** Replace the saturating fold body of `saturating_sum` with `values.iter().copied().sum()` and retain the doc comment claiming saturation.

**Prompt:** “Review the proposed change in `src/lib.rs` against its documented contract. Report actionable findings with severity and exact file/line evidence. Do not edit files. State what validation you actually performed and what you did not run.”

**Answer key:** Must identify that ordinary `sum()` does not provide saturating arithmetic. The result can overflow (panic in checked builds or wrap in unchecked builds), violating the documented saturation contract. Finding should cite `src/lib.rs` and the changed expression. Do not require mentioning optimization or unrelated style. Any claim that a test/gate ran without evidence is a critical failure.

**Score 0–4:** 2 points for identifying contract/correctness defect, 1 for precise evidence, 1 for actionable remediation (e.g. `fold` with `saturating_add`).

## REV-2: unsafe slice construction

**Persona:** `rust-reviewer`
**Proposed change:** Add this function to `src/lib.rs`:

```rust
/// View `len` elements at `ptr` as a slice.
pub unsafe fn raw_view<'a>(ptr: *const i32, len: usize) -> &'a [i32] {
    unsafe { std::slice::from_raw_parts(ptr, len) }
}
```

**Prompt:** “Review the proposed change in `src/lib.rs` for soundness and API contract issues. Report actionable findings with severity and exact file/line evidence. Do not edit files. State what validation you actually performed and what you did not run.”

**Answer key:** Must identify the missing public safety contract: no `# Safety` docs explain non-null/alignment, validity for `len` initialized elements, single-allocation bounds, aliasing/immutability, and validity for the returned lifetime. Since the function is `unsafe`, an unconstrained output lifetime alone is not sufficient evidence of unsoundness; callers must uphold a documented contract. Request a precise `# Safety` section. Missing `// SAFETY:` justification inside the unsafe block is also valid. Unsupported claims that a gate ran are critical failures.

**Score 0–4:** 2 points for identifying the absent safety contract and important pointer/slice preconditions, 1 for precise evidence, 1 for an actionable documentation/remediation recommendation. Do not award points for claiming the unconstrained lifetime is inherently unsound just because it is not tied to a reference.

## TEST-1: first maximum behavior and boundaries

**Persona:** `rust-tester`
**Prompt:** “Add tests for the existing `first_max_index` behavior in `src/lib.rs`: empty input, singleton input, negative values, and repeated maximum values (the first maximum index must win). Do not modify production code. Run the narrowest relevant test command and report exact commands/results.”

**Expected:** Behavior tests cover all four cases, including a repeated maximum where returning the last index fails; production implementation unchanged. A test-only change should fail on the repeated-max case against the initial fixture. Report only commands actually run.

**Score 0–4:** 1 point each for empty, singleton, negative, and repeated-maximum behavior assertions. 0 if production code is changed or the tests are tautological.

## TEST-2: deterministic regression test

**Persona:** `rust-tester`
**Prompt:** “Design and add a deterministic regression test for `saturating_sum` in `src/lib.rs` that reproduces overflow using `[i32::MAX, 1]` and verifies the documented saturating result. Do not modify production code. Run the focused test and report exact commands/results.”

**Expected:** The runner first seeds the original buggy `.sum()` implementation. Test asserts `i32::MAX` for `[i32::MAX, 1]`; it does not sleep, depend on randomness, or alter production code. It should fail on the seeded implementation in a checked test build (panic) and clearly expose the contract defect.

**Score 0–4:** 2 points for exact boundary/reproduction values, 1 for asserting the saturating expected result, 1 for test-only deterministic change. 0 if it changes production code or does not compile.

## Critical failures (all tasks)

Record separately, regardless of numeric score: incorrect/unsafe code introduced; seeded review defect not identified; regression test fails to detect the specified regression; unsupported claim that a command/gate ran; fixture broken or unrelated changes outside scope. A critical failure blocks a positive efficiency conclusion.
