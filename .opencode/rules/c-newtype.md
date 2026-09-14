# c-newtype

> Use Newtypes to enforce semantic distinctions and encapsulate validation.

## Why It Matters
Primitive obsession (passing raw `u64`, `String`, etc.) leads to swapped argument bugs and prevents compile-time safety. Newtypes have zero runtime overhead (`#[repr(transparent)]`).

## Bad
```rust
// Easy to accidentally swap userId and accountId!
fn transfer(user_id: u64, account_id: u64, amount: u64) {}
```

## Good
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[repr(transparent)]
pub struct UserId(pub u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[repr(transparent)]
pub struct AccountId(pub u64);

// Compile error if arguments are mixed up
fn transfer(user: UserId, account: AccountId, amount: u64) {}
```

## See Also
- [m-avoid-wrappers](m-avoid-wrappers.md) - Avoid unnecessary smart pointers
