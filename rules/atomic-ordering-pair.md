# atomic-ordering-pair
 
> Synchronize inter-thread state using matching `Release` stores and `Acquire` loads; avoid lazy `SeqCst` and unjustified `Relaxed`.

## Why It Matters
Atomic operations establish causal memory relationships across threads. Using `Ordering::SeqCst` everywhere incurs unnecessary memory barrier penalties on weakly ordered architectures (ARM, RISC-V). Conversely, using `Ordering::Relaxed` across threads without formal proof of independence causes subtle memory reordering bugs and data races.

## Bad
```rust
use std::sync::atomic::{AtomicBool, Ordering};

static READY: AtomicBool = AtomicBool::new(false);
static mut DATA: u64 = 0;

// Thread 1: Writer
unsafe { DATA = 42; }
// BUG: Relaxed allows the write to DATA to be reordered AFTER the flag!
READY.store(true, Ordering::Relaxed);

// Thread 2: Reader
if READY.load(Ordering::Relaxed) {
    // DATA read may see uninitialized or stale data!
    let val = unsafe { DATA };
}
```

## Good
```rust
use std::sync::atomic::{AtomicBool, Ordering};

static READY: AtomicBool = AtomicBool::new(false);
static mut DATA: u64 = 0;

// Thread 1: Release ensures all prior writes are visible to Acquire
unsafe { DATA = 42; }
READY.store(true, Ordering::Release);

// Thread 2: Acquire synchronizes with Release, establishing happens-before
if READY.load(Ordering::Acquire) {
    let val = unsafe { DATA };
    assert_eq!(val, 42);
}
```

## When Acceptable
`Ordering::Relaxed` is strictly acceptable for monotonic counters (e.g., metric counters, IDs) where no other memory operations depend on its ordering.
