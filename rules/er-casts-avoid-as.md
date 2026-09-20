# er-casts-avoid-as

> Avoid numeric `as` casts that silently truncate or change sign; prefer `TryFrom`, `TryInto`, or lossless conversions.

## Why It Matters
The `as` operator performs silent truncation when casting a wider integer to a narrower one (e.g., `1000u32 as u8` becomes `232`), or flips negative values to enormous positives (`-1i32 as u32`). These silent wraps introduce critical vulnerabilities and logic bugs. `TryFrom` makes overflow explicit and recoverable.

## Bad
```rust
fn process_packet(length: usize) {
    // BUG: Silently truncates if length > 65535!
    let packet_size = length as u16;
    send_raw(packet_size);
}

fn adjust_offset(offset: i64) {
    // BUG: Negative offset silently wraps to a huge positive index!
    let index = offset as usize;
    lookup(index);
}
```

## Good
```rust
use std::convert::TryInto;

fn process_packet(length: usize) -> Result<(), &'static str> {
    // Fails safely if length exceeds u16 limits
    let packet_size: u16 = length.try_into().map_err(|_| "packet too large")?;
    send_raw(packet_size);
    Ok(())
}

fn adjust_offset(offset: i64) -> Option<usize> {
    usize::try_from(offset).ok()
}
```

## When Acceptable
Lossless widening conversions (e.g., `u8 as u32`, `u16 as u64`) or pointer-to-integer casts in low-level FFI code where `as` is well-defined and cannot truncate.
