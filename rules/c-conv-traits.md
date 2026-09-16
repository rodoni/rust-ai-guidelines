# c-conv-traits

> Implement standard conversion traits (`From`, `TryFrom`, `AsRef`, `AsMut`) instead of bespoke ad-hoc methods.

## Why It Matters
Rust's standard conversion traits integrate seamlessly with generic bounds (`T: Into<U>`, `T: AsRef<Path>`). Custom methods like `to_my_type()` or `parse_str()` force callers to remember bespoke names and prevent your types from participating in standard ecosystem combinators.

## Bad
```rust
pub struct UserId(u64);

impl UserId {
    // Non-standard ad-hoc conversion method
    pub fn from_u64(val: u64) -> Self {
        Self(val)
    }
    pub fn to_u64(&self) -> u64 {
        self.0
    }
}
```

## Good
```rust
pub struct UserId(u64);

// Idiomatic From automatically provides Into<UserId> for u64
impl From<u64> for UserId {
    fn from(val: u64) -> Self {
        Self(val)
    }
}

// Fallible conversions use TryFrom
impl TryFrom<&str> for UserId {
    type Error = ParseIdError;
    fn try_from(s: &str) -> Result<Self, Self::Error> {
        s.parse::<u64>().map(Self).map_err(|_| ParseIdError)
    }
}
```

## See Also
- [c-conv](c-conv.md) - Ad-hoc conversion naming conventions
- [c-newtype](c-newtype.md) - Newtypes for domain distinction
