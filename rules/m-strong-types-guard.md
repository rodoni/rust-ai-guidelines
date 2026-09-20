# m-strong-types-guard

> Enforce domain invariants upon type construction (*Parse, Don't Validate*).

## Why It Matters
Validating data repeatedly at every function call site is fragile; checks are easy to miss. Validating once inside a constructor and returning a dedicated typed wrapper establishes a runtime-validated invariant that the type can preserve for later operations.

## Bad
```rust
// Invariant checked repeatedly throughout codebase:
pub fn send_email(email: &str) -> Result<(), Error> {
    if !email.contains('@') {
        return Err(Error::InvalidEmail);
    }
    // ...
}

pub fn save_contact(email: &str) -> Result<(), Error> {
    if !email.contains('@') {
        return Err(Error::InvalidEmail);
    }
    // ...
}
```

## Good
```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct EmailAddress(String);

impl EmailAddress {
    // Parse once at the boundary:
    pub fn parse(raw: String) -> Result<Self, InvalidEmailError> {
        // Simplified example predicate; real validation should use the domain's
        // complete syntax and policy requirements.
        if raw.contains('@') && !raw.starts_with('@') {
            Ok(Self(raw))
        } else {
            Err(InvalidEmailError)
        }
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// Functions accept the validated type; zero repetitive checks needed:
pub fn send_email(email: &EmailAddress) { ... }
pub fn save_contact(email: &EmailAddress) { ... }
```

## See Also
- [c-newtype](c-newtype.md) - Newtypes for domain distinction
- [m-design-for-ai](m-design-for-ai.md) - Design types for AI comprehension
