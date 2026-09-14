# OpenCode Agent Instructions

Instructions for OpenCode / OpenCodeInterpreter working with Rust repositories.

## Low-Context Guidelines Protocol
Before generating or refactoring Rust code, refer to the atomic rule files under `rules/` or `.opencode/rules/`. Do not load entire books into context; load only the specific rule ID needed for the task.

### Available Agents / Personas
- **Lead**: High-level triage and modular architecture.
- **API Architect**: Follows `c-case`, `c-conv`, `c-common-traits`, `m-avoid-wrappers`, `m-init-builder`.
- **Perf Optimizer**: Follows `mem-with-capacity`, `mem-reuse-collections`, `m-box-dst`, `m-fast-hasher`.
- **Safety Auditor**: Follows `unsafe-safety-comment`, `unsafe-minimize-scope`, `m-unsound-prevention`, `m-panic-on-bug`.
- **Reviewer**: Follows `m-lint-override-expect`, `c-failure`, `m-design-for-ai`.

### Rules Directory
All concise rule files reside in `rules/`. When auditing code or generating APIs, match against rule IDs directly.
