---
name: rust-macros
description: >
  Metaprogramming and macro design rules based on Microsoft Macros (M-MACRO-*) and
  Rust API Guidelines (C-MACRO-*). Declarative hygiene, proc-macro architecture, and compilation speed.
---

# Rust Metaprogramming Guidelines

Best practices for writing maintainable, fast-compiling, and hygienic declarative and procedural macros.

## Rules Index

| Rule | Impact | Summary |
|---|---|---|
| [`m-macro-last-resort`](../../rules/m-macro-last-resort.md) | HIGH | Treat macros as a tool of last resort; prefer functions/traits. |
| [`m-example-over-proc`](../../rules/m-example-over-proc.md) | HIGH | Prefer `macro_rules!` over procedural macros to save clean build time. |
| [`m-proc-impl`](../../rules/m-proc-impl.md) | HIGH | Factor proc macro AST logic into a unit-testable internal crate. |
| [`m-macro-helpers`](../../rules/m-macro-helpers.md) | HIGH | Re-export external macro dependencies under `#[doc(hidden)] pub mod _private`. |
