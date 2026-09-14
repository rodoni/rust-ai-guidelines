# unsafe-safety-comment

> Every `unsafe` block must have an explicit `// SAFETY:` comment justifying why it is sound.

## Why It Matters
Without a `// SAFETY:` comment, reviewers and AI agents cannot verify whether the author considered the necessary invariants, making code audits and maintenance unsafe.

## Bad
```rust
// No explanation of why this raw pointer dereference is valid
let val = unsafe { *ptr };
```

## Good
```rust
// SAFETY: `ptr` was verified to be non-null above, properly aligned to u32,
// and points to an initialized value that outlives this function call.
let val = unsafe { *ptr };
```

## Mandatory Elements
A good `// SAFETY:` comment specifies:
1. Pointer validity / alignment / non-null guarantees.
2. Invariant preservation.
3. Lifetime or alias uniqueness assurances.
