# c-case

> Follow RFC 430 casing conventions strictly.

## Why It Matters
Inconsistent casing violates community expectations, impairs discoverability, and triggers compiler lints.

## Bad
```rust
// Inconsistent casing
struct user_profile;
fn CalculateTax() {}
const max_retries: u32 = 5;
enum status { ActiveNow, InActive }
```

## Good
```rust
// Idiomatic Rust casing (RFC 430)
struct UserProfile;         // UpperCamelCase
fn calculate_tax() {}       // snake_case
const MAX_RETRIES: u32 = 5; // SCREAMING_SNAKE_CASE
enum Status {               // UpperCamelCase
    ActiveNow,
    Inactive,
}
```

## See Also
- [c-getter](c-getter.md) - Getter naming conventions
- [m-weasel-words](m-weasel-words.md) - Avoid vague names
