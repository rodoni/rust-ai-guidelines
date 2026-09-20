---
name: rust-agentic-workflow
description: >
  Core agentic development workflows for Rust based on the Tweag Agentic Coding Handbook.
  Enforces Spec-First planning, atomic steps, deterministic verification gates, TDD, and systematic debugging.
---

# Rust Agentic Workflows Guidelines

Methodologies and operational workflows designed for AI coding agents and Rust developers to prevent hallucination, borrow checker loops, and unverified code changes.

## Rules Index

| Rule | Impact | Summary |
|---|---|---|
| [`wf-spec-first`](../../rules/wf-spec-first.md) | CRITICAL | Design types, traits, contracts, and invariants before modifying code. |
| [`wf-atomic-steps`](../../rules/wf-atomic-steps.md) | HIGH | Execute changes in incremental, testable, and reversible steps. |
| [`wf-verification-gates`](../../rules/wf-verification-gates.md) | CRITICAL | Validate code via `cargo fmt`, `check`, `clippy -D warnings`, and `test`. |
| [`wf-tdd-loop`](../../rules/wf-tdd-loop.md) | HIGH | Write failing tests before implementing features or fixes (Red-Green-Refactor). |
| [`wf-debug-systematic`](../../rules/wf-debug-systematic.md) | HIGH | Isolate bugs through minimal reproduction and evidence; never guess randomly. |
