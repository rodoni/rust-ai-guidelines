---
name: rust-guidelines
description: >
  Zero-overhead, low-context Rust engineering guidelines combining Microsoft Pragmatic
  Rust Guidelines, Rust API Guidelines, Mara Bos Atomics and Locks, Effective Rust,
  and Programming Rust. Contains prioritized rules for API design, memory optimization,
  concurrency, async, unsafe correctness, macros, FFI, testing, and AI-ready code.
license: MIT
metadata:
  version: "1.2.0"
  sources:
    - https://microsoft.github.io/rust-guidelines/
    - https://rust-lang.github.io/api-guidelines/
    - https://mara.nl/atomics/
    - https://www.lurklurk.org/effective-rust/
    - Programming Rust (O'Reilly)
    - https://tweag.github.io/agentic-coding-handbook/workflows/
---

# Rust Guidelines Master Hub

Ultra-concise, low-context engineering rules for AI coding agents and Rust developers. Prioritized by impact to prevent token waste and hallucinations.

## Quick Index by Priority

| Priority | Category | Prefix | Impact | Skill File |
|---|---|---|---|---|
| 1 | **Agentic Workflows** | `wf-` | CRITICAL | [rust-agentic-workflow](../rust-agentic-workflow/SKILL.md) |
| 2 | **Safety & Correctness** | `unsafe-`, `m-unsound-`, `m-panic-`, `er-casts-` | CRITICAL | [rust-safety](../rust-safety/SKILL.md) |
| 3 | **Concurrency & Atomics** | `atomic-`, `sync-` | CRITICAL | [rust-concurrency](../rust-concurrency/SKILL.md) |
| 4 | **API & Type Ergonomics** | `c-`, `m-`, `er-` | HIGH | [rust-api](../rust-api/SKILL.md) |
| 5 | **Performance & Memory** | `mem-`, `m-`, `sys-` | HIGH | [rust-perf](../rust-perf/SKILL.md) |
| 6 | **Apps, Resilience & AI** | `m-` | MEDIUM | [rust-resilience-app](../rust-resilience-app/SKILL.md) |
| 7 | **Metaprogramming & Macros**| `m-macro-`, `m-proc-`, `m-example-` | MEDIUM | [rust-macros](../rust-macros/SKILL.md) |
| 8 | **Testing & Verification** | `test-` | HIGH | [rust-testing](../rust-testing/SKILL.md) |
| 9 | **Native FFI** | `m-ffi-`, `m-isolate-` | SPECIALIZED | [rust-ffi](../rust-ffi/SKILL.md) |

---

## All Rules Index (Load rules on-demand)

### 1. Safety & Correctness (CRITICAL)
- [`unsafe-safety-comment`](../../rules/unsafe-safety-comment.md) - Mandatory `// SAFETY:` explanation on every `unsafe` block.
- [`unsafe-minimize-scope`](../../rules/unsafe-minimize-scope.md) - Restrict `unsafe` strictly to the single triggering operation.
- [`m-unsound-prevention`](../../rules/m-unsound-prevention.md) - Safe public APIs wrapping `unsafe` must be 100% sound under all inputs.
- [`m-panic-on-bug`](../../rules/m-panic-on-bug.md) - Panics are strictly for programming bugs; use `Result` for runtime fallibility.
- [`m-errors-canonical`](../../rules/m-errors-canonical.md) - Library errors are situation-specific structs with backtraces and query methods.
- [`c-dtor-fail`](../../rules/c-dtor-fail.md) - Destructors (`Drop` trait) must never panic.
- [`m-avoid-statics`](../../rules/m-avoid-statics.md) - Avoid mutable global statics; pass state explicitly.
- [`m-strong-types-guard`](../../rules/m-strong-types-guard.md) - Enforce domain invariants upon type construction (*Parse, Don't Validate*).
- [`er-casts-avoid-as`](../../rules/er-casts-avoid-as.md) - Avoid lossy numeric `as` casts; use `TryFrom`/`TryInto` or checked methods.
- [`er-raii-guard`](../../rules/er-raii-guard.md) - Encapsulate state cleanup and resource release into RAII guards (`Drop`).

### 2. Concurrency & Atomics (CRITICAL)
- [`atomic-ordering-pair`](../../rules/atomic-ordering-pair.md) - Choose atomic orderings from the algorithm's synchronization relationship.
- [`sync-avoid-spinlock`](../../rules/sync-avoid-spinlock.md) - Avoid unbounded spinning; prefer blocking or bounded adaptive synchronization.
- [`sync-cacheline-padding`](../../rules/sync-cacheline-padding.md) - Consider padding concurrently mutated hot variables to reduce false sharing when justified.
- [`sync-lock-hierarchy`](../../rules/sync-lock-hierarchy.md) - Enforce deterministic lock acquisition order to prevent deadlocks.
- [`atomic-cas-weak-loops`](../../rules/atomic-cas-weak-loops.md) - Prefer `compare_exchange_weak` in atomic retry loops.

### 3. API & Ergonomics (HIGH)
- [`c-case`](../../rules/c-case.md) - Strict RFC 430 casing conventions.
- [`c-conv`](../../rules/c-conv.md) - Naming ad-hoc conversions (`as_` borrow, `to_` copy, `into_` move).
- [`c-getter`](../../rules/c-getter.md) - Omit `get_` prefix on standard accessors.
- [`c-common-traits`](../../rules/c-common-traits.md) - Derive standard traits (`Debug`, `Clone`, `Default`, `Eq`, `Hash`).
- [`c-send-sync`](../../rules/c-send-sync.md) - Ensure public types are `Send + Sync` where sound.
- [`c-newtype`](../../rules/c-newtype.md) - Use Newtypes to prevent primitive obsession and swap bugs.
- [`c-sealed`](../../rules/c-sealed.md) - Use the sealed trait pattern to protect public traits from semver breaks.
- [`m-weasel-words`](../../rules/m-weasel-words.md) - Eliminate vague names (`Helper`, `Manager`, `Data`, `Info`).
- [`m-regular-fn`](../../rules/m-regular-fn.md) - Prefer module functions over empty utility structs.
- [`m-avoid-wrappers`](../../rules/m-avoid-wrappers.md) - Avoid implementation-detail wrappers; allow them when ownership or dynamic dispatch requires it.
- [`m-di-hierarchy`](../../rules/m-di-hierarchy.md) - Concrete types > Generics with bounds > `dyn Trait`.
- [`m-init-builder`](../../rules/m-init-builder.md) - Use the Builder pattern with fallible `.build()` for complex structs.
- [`m-services-clone`](../../rules/m-services-clone.md) - Service/client structs implement cheap `Clone` via internal `Arc`.
- [`m-async-fn`](../../rules/m-async-fn.md) - Use `async fn` syntax instead of manually returning `impl Future`.
- [`c-conv-traits`](../../rules/c-conv-traits.md) - Implement standard conversion traits (`From`, `TryFrom`, `AsRef`).
- [`c-custom-type`](../../rules/c-custom-type.md) - Arguments convey meaning via domain types/enums, avoiding bool flags.
- [`c-deref`](../../rules/c-deref.md) - Only smart pointers implement `Deref` / `DerefMut`.
- [`c-generic`](../../rules/c-generic.md) - Functions minimize assumptions by using generic bounds (`impl AsRef<Path>`).
- [`c-smart-ptr`](../../rules/c-smart-ptr.md) - Smart pointers do not introduce inherent methods.
- [`m-dont-leak-types`](../../rules/m-dont-leak-types.md) - Do not expose unexported foreign crate types in public signatures.
- [`er-typestate-pattern`](../../rules/er-typestate-pattern.md) - Express lifecycle states in generic phantom types (Typestate).
- [`er-reexport-dependencies`](../../rules/er-reexport-dependencies.md) - Re-export third-party types that appear in public API signatures.
- [`er-closure-traits`](../../rules/er-closure-traits.md) - Accept the least restrictive closure trait required by the call pattern.

### 4. Performance & Memory (HIGH)
- [`mem-with-capacity`](../../rules/mem-with-capacity.md) - Reserve capacity when a reliable estimate makes it worthwhile.
- [`mem-reuse-collections`](../../rules/mem-reuse-collections.md) - Clear and reuse buffers in loops to prevent allocator churn.
- [`m-box-dst`](../../rules/m-box-dst.md) - Consider `Box<[T]>` or `Box<str>` for frequently instantiated, immutable internal sequences.
- [`m-shrink-to-fit`](../../rules/m-shrink-to-fit.md) - Consider shrinking long-lived collections after measuring growth patterns.
- [`m-fast-hasher`](../../rules/m-fast-hasher.md) - Use `ahash` or `foldhash` for internal HashMaps.
- [`m-async-stack-size`](../../rules/m-async-stack-size.md) - Measure and reduce large state held across `.await`; boxing is one option.
- [`m-yield-points`](../../rules/m-yield-points.md) - Insert cooperative yield points in CPU-bound async loops.
- [`sys-struct-field-ordering`](../../rules/sys-struct-field-ordering.md) - Order fields deliberately in layout-sensitive performance-critical structs.
- [`sys-iterator-zero-allocation`](../../rules/sys-iterator-zero-allocation.md) - Chain iterators lazily without intermediate heap allocations.
- [`sys-dispatch-tradeoff`](../../rules/sys-dispatch-tradeoff.md) - Weigh static and dynamic dispatch against code size, compile time, and ergonomics.

### 5. Apps, Resilience & AI (MEDIUM)
- [`m-mimalloc-apps`](../../rules/m-mimalloc-apps.md) - Evaluate `mimalloc` when representative benchmarks justify it.
- [`m-cargo-workspace`](../../rules/m-cargo-workspace.md) - Centralize all dependency versions under `[workspace.dependencies]`.
- [`m-smaller-crates`](../../rules/m-smaller-crates.md) - Decompose monolithic crates into single-responsibility workspace crates.
- [`m-app-error`](../../rules/m-app-error.md) - Aggregate errors at application boundaries; public libraries expose typed errors.
- [`m-mockable-syscalls`](../../rules/m-mockable-syscalls.md) - Design domain logic "sans I/O" or abstract behind traits.
- [`m-test-util`](../../rules/m-test-util.md) - Gate test fixtures and fakes behind `feature = "test-util"`.
- [`c-failure`](../../rules/c-failure.md) - Document `# Errors`, `# Panics`, and `# Safety` when applicable.
- [`m-design-for-ai`](../../rules/m-design-for-ai.md) - Design code for AI comprehension: strict types and runnable doc tests.
- [`m-lint-override-expect`](../../rules/m-lint-override-expect.md) - Use `#[expect]` over `#[allow]` to prevent zombie lints.
- [`m-log-not-print`](../../rules/m-log-not-print.md) - Use telemetry for diagnostics; reserve stdout/stderr for deliberate presentation output.
- [`m-log-structured`](../../rules/m-log-structured.md) - Structured telemetry with key-value fields rather than string interpolation.
- [`m-features-additive`](../../rules/m-features-additive.md) - Prefer additive features; diagnose valid exclusive backend combinations.

### 6. Metaprogramming & Macros (MEDIUM)
- [`m-macro-last-resort`](../../rules/m-macro-last-resort.md) - Treat macros as a last resort; prefer functions and traits.
- [`m-example-over-proc`](../../rules/m-example-over-proc.md) - Prefer declarative `macro_rules!` over procedural macros.
- [`m-proc-impl`](../../rules/m-proc-impl.md) - Separate procedural macro AST logic into a testable internal crate.
- [`m-macro-helpers`](../../rules/m-macro-helpers.md) - Re-export external macro dependencies under `#[doc(hidden)] pub mod _private`.

### 7. Native FFI (SPECIALIZED)
- [`m-ffi-translates`](../../rules/m-ffi-translates.md) - FFI crates only translate types; core logic belongs in pure Rust crates.
- [`m-isolate-dll-state`](../../rules/m-isolate-dll-state.md) - Return opaque pointers and isolate dynamic library state.
- [`m-ffi-naming`](../../rules/m-ffi-naming.md) - Exported C-ABI functions should use an explicit, collision-resistant namespace.

### 8. Agentic Workflows & Methodology (CRITICAL)
- [`wf-spec-first`](../../rules/wf-spec-first.md) - Design types, traits, contracts, and invariants before modifying code.
- [`wf-atomic-steps`](../../rules/wf-atomic-steps.md) - Execute changes in small, testable, and reversible steps.
- [`wf-verification-gates`](../../rules/wf-verification-gates.md) - Validate code via `cargo fmt`, `check`, `clippy -D warnings`, and `test`.
- [`wf-tdd-loop`](../../rules/wf-tdd-loop.md) - Write failing tests before implementing features or fixes (Red-Green-Refactor).
- [`wf-debug-systematic`](../../rules/wf-debug-systematic.md) - Isolate bugs through minimal reproduction and evidence; never guess randomly.

### 9. Testing & Verification (HIGH)
- [`test-property-based`](../../rules/test-property-based.md) - Use property-based testing (`proptest`) for pure logic, codecs, and invariants.
- [`test-assert-error-variants`](../../rules/test-assert-error-variants.md) - Assert specific error enum variants with `matches!`, never just `.is_err()`.
- [`test-deterministic-no-sleep`](../../rules/test-deterministic-no-sleep.md) - Eliminate wall-clock `sleep`; use simulated time or `tokio::time::pause()`.
- [`test-fakes-over-heavy-mocks`](../../rules/test-fakes-over-heavy-mocks.md) - Prefer simple in-memory fakes over complex dynamic mocking frameworks.
- [`test-behavior-not-internals`](../../rules/test-behavior-not-internals.md) - Test observable module contracts and invariants, not ephemeral private helpers.
- [`test-snapshot-for-complex-data`](../../rules/test-snapshot-for-complex-data.md) - Use snapshot testing (`insta`) for large structs, ASTs, and CLI output.

