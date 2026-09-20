# sys-struct-field-ordering

> In layout-sensitive performance-critical structs, order fields from largest alignment to smallest when the representation makes ordering meaningful.

## Why It Matters
Hardware alignment requires values of size $N$ to reside at memory addresses divisible by $N$. In unoptimized or `#[repr(C)]` layouts, interleaving 1-byte booleans with 8-byte pointers creates up to 7 bytes of dead padding per field, inflating cache footprint and degrading memory bandwidth in large collections.

## Bad
```rust
#[repr(C)]
pub struct PacketHeader {
    pub is_valid: bool,    // 1 byte + 7 bytes PADDING!
    pub timestamp: u64,    // 8 bytes
    pub flag: u8,          // 1 byte + 7 bytes PADDING!
    pub payload_len: u64,  // 8 bytes
} // Total: 32 bytes (14 bytes wasted on padding)
```

## Good
```rust
// Order: largest alignment/size down to smallest
#[repr(C)]
pub struct PacketHeader {
    pub timestamp: u64,    // 8 bytes
    pub payload_len: u64,  // 8 bytes
    pub is_valid: bool,    // 1 byte
    pub flag: u8,          // 1 byte + 6 bytes trailing padding
} // Total: 24 bytes (saved 25% memory per element in a Vec!)

// Tip: For `repr(C)` and other layout-sensitive structs, explicit ordering
// documents the intended layout. `repr(Rust)` does not promise stable field order.
```

## When Acceptable
Small one-off structs not stored in large vectors, or domain models where logical field grouping is prioritized over micro-optimizations.
