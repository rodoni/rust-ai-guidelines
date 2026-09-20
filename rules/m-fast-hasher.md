# m-fast-hasher

> Use a fast non-cryptographic hasher (`ahash` or `foldhash`) for internal HashMaps.

## Why It Matters
The standard library `std::collections::HashMap` uses SipHash 1-3 to defend against HashDoS attacks. For internal, trusted keys, a faster non-cryptographic hasher may reduce lookup and insertion cost, but the result depends on key types, hardware, and workload.

## Bad
```rust
use std::collections::HashMap;

// Uses default SipHash on internal high-frequency lookups
let mut cache: HashMap<u64, Item> = HashMap::default();
```

## Good
```rust
use ahash::AHashMap; // Or foldhash / rustc-hash for integer keys

// Benchmark representative lookups before standardizing this choice.
let mut cache: AHashMap<u64, Item> = AHashMap::default();
```

## When Acceptable
Keep SipHash (standard `HashMap`) when keys originate from untrusted external network clients to avoid HashDoS vulnerabilities.
