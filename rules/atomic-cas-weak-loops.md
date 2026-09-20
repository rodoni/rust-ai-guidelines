# atomic-cas-weak-loops

> Use `compare_exchange_weak` instead of `compare_exchange` inside retry loops.

## Why It Matters
On architectures using Load-Linked/Store-Conditional (LL/SC) primitives (ARM, RISC-V, PowerPC), `compare_exchange` requires an internal retry loop to mask spurious failures. Calling `compare_exchange` inside your own loop creates a nested loop. Using `compare_exchange_weak` compiles directly to single LL/SC pairs, significantly reducing instruction latency.

## Bad
```rust
use std::sync::atomic::{AtomicUsize, Ordering};

pub fn atomic_update(atomic: &AtomicUsize, val: usize) {
    let mut current = atomic.load(Ordering::Relaxed);
    // SUBOPTIMAL: compare_exchange incurs an extra internal loop on ARM/RISC-V!
    while let Err(actual) = atomic.compare_exchange(
        current,
        current.max(val),
        Ordering::Release,
        Ordering::Relaxed,
    ) {
        current = actual;
    }
}
```

## Good
```rust
use std::sync::atomic::{AtomicUsize, Ordering};

pub fn atomic_update(atomic: &AtomicUsize, val: usize) {
    let mut current = atomic.load(Ordering::Relaxed);
    // OPTIMAL: Spurious failures are naturally absorbed by the outer loop
    while let Err(actual) = atomic.compare_exchange_weak(
        current,
        current.max(val),
        Ordering::Release,
        Ordering::Relaxed,
    ) {
        current = actual;
        std::hint::spin_loop();
    }
}
```

## When Acceptable
Use strong `compare_exchange` when you are executing a single one-shot attempt without a retry loop and cannot tolerate spurious failures.
