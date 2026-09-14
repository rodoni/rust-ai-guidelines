# m-lint-override-expect

> Use `#[expect(clippy::...)]` instead of `#[allow(clippy::...)]` for deliberate lint suppressions.

## Why It Matters
`#[allow]` silences a lint forever, even after subsequent refactoring eliminates the triggering condition. `#[expect]` alerts you when the suppressed issue no longer occurs, preventing dead lint suppressions.

## Bad
```rust
// Silenced forever, even if the code later stops needing it
#[allow(clippy::too_many_arguments)]
fn init(...) {}
```

## Good
```rust
// Compiler warns if the function signature is later reduced to <=7 arguments
#[expect(clippy::too_many_arguments, reason = "Legacy FFI compatibility requires 8 parameters")]
fn init(...) {}
```
