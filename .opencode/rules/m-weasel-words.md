# m-weasel-words

> Eliminate vague "weasel words" (Helper, Manager, Common, Data, Info) from names.

## Why It Matters
Vague suffixes obscure responsibility, encourage messy god-objects, and confuse human developers and AI coding agents.

## Bad
```rust
struct SessionManagerHelper;
struct UserDataManager;
fn process_info_data() {}
```

## Good
```rust
// Clear, focused domain models
struct SessionStore;
struct UserRepository;
fn process_credentials() {}
```

## See Also
- [c-case](c-case.md) - Casing conventions
