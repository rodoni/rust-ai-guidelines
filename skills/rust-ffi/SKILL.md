---
name: rust-ffi
description: >
  Native C-ABI interoperability guidelines based on Microsoft FFI rules (M-FFI-*).
  Covers state isolation, DLL safety, sound type conversions, and boundary separation.
---

# Rust FFI Guidelines

Focused rules for interfacing safely between Rust and C/C++ or external native runtimes.

## Rules Index

| Rule | Impact | Summary |
|---|---|---|
| [`m-ffi-translates`](../../rules/m-ffi-translates.md) | CRITICAL | FFI crates only translate types; core logic remains in pure Rust crates. |
| [`m-isolate-dll-state`](../../rules/m-isolate-dll-state.md) | HIGH | Return opaque boxed pointers; never use shared mutable global statics in DLLs. |
| [`m-ffi-naming`](../../rules/m-ffi-naming.md) | HIGH | Exported C-ABI functions should follow `<crate>_<type>_<method>` naming. |
| [`unsafe-safety-comment`](../../rules/unsafe-safety-comment.md) | CRITICAL | Mandatory `// SAFETY:` explaining raw pointer validity and alignment. |
