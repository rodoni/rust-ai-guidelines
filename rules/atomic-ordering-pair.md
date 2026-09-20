# atomic-ordering-pair
 
> Choose atomic orderings from the algorithm's synchronization relationship; avoid unjustified `Relaxed` and `SeqCst`.

## Why It Matters
Atomic operations establish causal memory relationships across threads. `Release`/`Acquire` is a common publication pattern, but RMW operations, release sequences, locks, semaphores, and counters may require different orderings. `Relaxed` is valid only when no other memory access depends on that operation; `SeqCst` should be chosen deliberately rather than mechanically.

## Bad
```rust
use std::sync::atomic::{AtomicBool, Ordering};

struct Shared {
    ready: AtomicBool,
    data: std::sync::atomic::AtomicU64,
}

// Assume `shared` is safely shared between the two threads.
let shared = Shared {
    ready: AtomicBool::new(false),
    data: std::sync::atomic::AtomicU64::new(0),
};

// Thread 1: Writer
shared.data.store(42, Ordering::Relaxed);
// BUG: Relaxed allows the write to DATA to be reordered AFTER the flag!
shared.ready.store(true, Ordering::Relaxed);

// Thread 2: Reader
if shared.ready.load(Ordering::Relaxed) {
    // The flag does not publish the preceding data store.
    let val = shared.data.load(Ordering::Relaxed);
}
```

## Good
```rust
use std::sync::atomic::{AtomicBool, Ordering};

let shared = Shared {
    ready: AtomicBool::new(false),
    data: std::sync::atomic::AtomicU64::new(0),
};

// Thread 1: Release ensures all prior writes are visible to Acquire
shared.data.store(42, Ordering::Relaxed);
shared.ready.store(true, Ordering::Release);

// Thread 2: Acquire synchronizes with Release, establishing happens-before
if shared.ready.load(Ordering::Acquire) {
    let val = shared.data.load(Ordering::Relaxed);
    assert_eq!(val, 42);
}
```

## When Acceptable
`Ordering::Relaxed` is acceptable for independent monotonic counters or values when the algorithm proves that no other memory operation depends on their ordering.
