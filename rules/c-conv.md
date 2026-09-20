# c-conv

> Name ad-hoc conversions following `as_`, `to_`, and `into_` conventions.

## Why It Matters
Predictable prefixing immediately tells callers the cost and ownership semantics of the conversion without reading internal docs.

## Convention Summary
- `as_`: Free/cheap borrowed-to-borrowed conversion (`&T -> &U`).
- `to_`: A conversion that may allocate or copy, commonly borrowed-to-owned (`&T -> U`), but also borrowed-to-borrowed or owned-to-owned when that matches the API semantics.
- `into_`: Value-consuming conversion (`T -> U`).

## Bad
```rust
impl Buffer {
    // Ambiguous naming: does it clone, borrow, or consume?
    fn slice(&self) -> &[u8] { &self.raw }
    fn string(&self) -> String { String::from_utf8_lossy(&self.raw).into_owned() }
    fn vector(self) -> Vec<u8> { self.raw }
}
```

## Good
```rust
impl Buffer {
    fn as_bytes(&self) -> &[u8] { &self.raw }        // Free borrow
    fn to_string_lossy(&self) -> String { ... }     // Allocation/copy
    fn into_vec(self) -> Vec<u8> { self.raw }       // Consumes self
}
```

## See Also
- [c-getter](c-getter.md) - Getter naming conventions
