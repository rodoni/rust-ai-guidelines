# m-ffi-naming

> Exported C-ABI functions should follow `<crate>_<type>_<method>` naming.

## Why It Matters
C has no namespaces. If multiple dynamic libraries or C dependencies export generic names like `create()`, `destroy()`, or `init()`, the linker encounters catastrophic symbol collisions at load time. Explicit namespacing prevents collision and clarifies foreign ownership.

The examples use the Rust 2024 form `#[unsafe(no_mangle)]`; older editions may
accept `#[no_mangle]` without the explicit unsafe attribute.

## Bad
```rust
// Global namespace collision waiting to happen:
#[unsafe(no_mangle)]
pub extern "C" fn init() { ... }

#[unsafe(no_mangle)]
pub extern "C" fn process_buffer(buf: *const u8, len: usize) -> i32 { ... }
```

## Good
```rust
// Prefixed with crate, domain type, and operation:
#[unsafe(no_mangle)]
pub extern "C" fn mycrate_engine_init() { ... }

#[unsafe(no_mangle)]
pub extern "C" fn mycrate_parser_process_buffer(buf: *const u8, len: usize) -> i32 { ... }
```

## See Also
- [m-ffi-translates](m-ffi-translates.md) - FFI crates translate types only
- [m-isolate-dll-state](m-isolate-dll-state.md) - Isolate DLL state
