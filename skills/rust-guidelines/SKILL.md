---
name: rust-guidelines
description: >
  Zero-overhead, low-context Rust engineering guidelines combining Microsoft Pragmatic
  Rust Guidelines and Rust API Guidelines. Contains prioritized rules for API design,
  memory optimization, async, unsafe correctness, macros, FFI, testing, and AI-ready code.
license: MIT
metadata:
  version: "1.0.0"
  sources:
    - https://microsoft.github.io/rust-guidelines/
    - https://rust-lang.github.io/api-guidelines/
---

# Rust Guidelines Master Hub

Ultra-concise, low-context engineering rules for AI coding agents and Rust developers. Prioritized by impact to prevent token waste and hallucinations.

## Quick Index by Priority

| Priority | Category | Prefix | Impact | Skill File |
|---|---|---|---|---|
| 1 | **Safety & Correctness** | `unsafe-`, `m-unsound-`, `m-panic-` | CRITICAL | [rust-safety](../rust-safety/SKILL.md) |
| 2 | **API & Type Ergonomics** | `c-`, `m-` | HIGH | [rust-api](../rust-api/SKILL.md) |
| 3 | **Performance & Memory** | `mem-`, `m-` | HIGH | [rust-perf](../rust-perf/SKILL.md) |
| 4 | **Apps, Resilience & AI** | `m-` | MEDIUM | [rust-resilience-app](../rust-resilience-app/SKILL.md) |
| 5 | **Metaprogramming & Macros**| `m-macro-`, `m-proc-`, `m-example-` | MEDIUM | [rust-macros](../rust-macros/SKILL.md) |
| 6 | **Native FFI** | `m-ffi-`, `m-isolate-` | SPECIALIZED | [rust-ffi](../rust-ffi/SKILL.md) |

---

## All Rules Index (Load rules on-demand)

### 1. Safety & Correctness (CRITICAL)
- [`unsafe-safety-comment`](../../rules/unsafe-safety-comment.md) - Mandatory `// SAFETY:` explanation on every `unsafe` block.
- [`unsafe-minimize-scope`](../../rules/unsafe-minimize-scope.md) - Restrict `unsafe` strictly to the single triggering operation.
- [`m-unsound-prevention`](../../rules/m-unsound-prevention.md) - Safe public APIs wrapping `unsafe` must be 100% sound under all inputs.
- [`m-panic-on-bug`](../../rules/m-panic-on-bug.md) - Panics are strictly for programming bugs; use `Result` for runtime fallibility.
- [`m-errors-canonical`](../../rules/m-errors-canonical.md) - Library errors must be typed enums via `thiserror`.
- [`c-dtor-fail`](../../rules/c-dtor-fail.md) - Destructors (`Drop` trait) must never panic.
- [`m-avoid-statics`](../../rules/m-avoid-statics.md) - Avoid mutable global statics; pass state explicitly.
- [`m-strong-types-guard`](../../rules/m-strong-types-guard.md) - Enforce domain invariants upon type construction (*Parse, Don't Validate*).

### 2. API & Ergonomics (HIGH)
- [`c-case`](../../rules/c-case.md) - Strict RFC 430 casing conventions.
- [`c-conv`](../../rules/c-conv.md) - Naming ad-hoc conversions (`as_` borrow, `to_` copy, `into_` move).
- [`c-getter`](../../rules/c-getter.md) - Omit `get_` prefix on standard accessors.
- [`c-common-traits`](../../rules/c-common-traits.md) - Derive standard traits (`Debug`, `Clone`, `Default`, `Eq`, `Hash`).
- [`c-send-sync`](../../rules/c-send-sync.md) - Ensure public types are `Send + Sync` where sound.
- [`c-newtype`](../../rules/c-newtype.md) - Use Newtypes to prevent primitive obsession and swap bugs.
- [`c-sealed`](../../rules/c-sealed.md) - Use the sealed trait pattern to protect public traits from semver breaks.
- [`m-weasel-words`](../../rules/m-weasel-words.md) - Eliminate vague names (`Helper`, `Manager`, `Data`, `Info`).
- [`m-regular-fn`](../../rules/m-regular-fn.md) - Prefer module functions over empty utility structs.
- [`m-avoid-wrappers`](../../rules/m-avoid-wrappers.md) - Never expose `Arc`/`Mutex`/`Box` in public signatures.
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

### 3. Performance & Memory (HIGH)
- [`mem-with-capacity`](../../rules/mem-with-capacity.md) - Always preallocate collection capacity when size is known.
- [`mem-reuse-collections`](../../rules/mem-reuse-collections.md) - Clear and reuse buffers in loops to prevent allocator churn.
- [`m-box-dst`](../../rules/m-box-dst.md) - Use `Box<[T]>` or `Box<str>` for immutable owned sequences.
- [`m-shrink-to-fit`](../../rules/m-shrink-to-fit.md) - Shrink collections after assembly in long-lived structs.
- [`m-fast-hasher`](../../rules/m-fast-hasher.md) - Use `ahash` or `foldhash` for internal HashMaps.
- [`m-async-stack-size`](../../rules/m-async-stack-size.md) - Box large buffers kept across `.await` points.
- [`m-yield-points`](../../rules/m-yield-points.md) - Insert cooperative yield points in CPU-bound async loops.

### 4. Apps, Resilience & AI (MEDIUM)
- [`m-mimalloc-apps`](../../rules/m-mimalloc-apps.md) - Configure `mimalloc` as the global allocator in application binaries.
- [`m-cargo-workspace`](../../rules/m-cargo-workspace.md) - Centralize all dependency versions under `[workspace.dependencies]`.
- [`m-smaller-crates`](../../rules/m-smaller-crates.md) - Decompose monolithic crates into single-responsibility workspace crates.
- [`m-app-error`](../../rules/m-app-error.md) - Use `anyhow` for top-level binaries; never in libraries.
- [`m-mockable-syscalls`](../../rules/m-mockable-syscalls.md) - Design domain logic "sans I/O" or abstract behind traits.
- [`m-test-util`](../../rules/m-test-util.md) - Gate test fixtures and fakes behind `feature = "test-util"`.
- [`c-failure`](../../rules/c-failure.md) - Mandatory `# Errors`, `# Panics`, and `# Safety` doc sections.
- [`m-design-for-ai`](../../rules/m-design-for-ai.md) - Design code for AI comprehension: strict types and runnable doc tests.
- [`m-lint-override-expect`](../../rules/m-lint-override-expect.md) - Use `#[expect]` over `#[allow]` to prevent zombie lints.
- [`m-log-not-print`](../../rules/m-log-not-print.md) - Production code uses telemetry (`tracing`/`log`), never `println!` or `dbg!`.
- [`m-log-structured`](../../rules/m-log-structured.md) - Structured telemetry with key-value fields rather than string interpolation.
- [`m-features-additive`](../../rules/m-features-additive.md) - Cargo features must be strictly additive; never mutually exclusive.

### 5. Metaprogramming & Macros (MEDIUM)
- [`m-macro-last-resort`](../../rules/m-macro-last-resort.md) - Treat macros as a last resort; prefer functions and traits.
- [`m-example-over-proc`](../../rules/m-example-over-proc.md) - Prefer declarative `macro_rules!` over procedural macros.
- [`m-proc-impl`](../../rules/m-proc-impl.md) - Separate procedural macro AST logic into a testable internal crate.
- [`m-macro-helpers`](../../rules/m-macro-helpers.md) - Re-export external macro dependencies under `#[doc(hidden)] pub mod _private`.

### 6. Native FFI (SPECIALIZED)
- [`m-ffi-translates`](../../rules/m-ffi-translates.md) - FFI crates only translate types; core logic belongs in pure Rust crates.
- [`m-isolate-dll-state`](../../rules/m-isolate-dll-state.md) - Return opaque pointers and isolate dynamic library state.
- [`m-ffi-naming`](../../rules/m-ffi-naming.md) - Exported C-ABI functions follow strict `<crate>_<type>_<method>` naming.
