# sync-avoid-spinlock

> Never implement busy-wait spinlocks in user space; use OS-backed blocking locks or futex primitives.

## Why It Matters
A user-space thread spinning in a tight `while test_and_set()` loop starves other threads of CPU execution. If the thread holding the lock is preempted by the OS scheduler, spinning threads burn 100% CPU waiting for a preempted thread, causing massive priority inversion, thermal throttling, and throughput collapse.

## Bad
```rust
use std::sync::atomic::{AtomicBool, Ordering};

pub struct NaiveSpinLock {
    locked: AtomicBool,
}

impl NaiveSpinLock {
    pub fn lock(&self) {
        // HAZARD: 100% CPU burn during contention; vulnerable to OS preemption!
        while self.locked.swap(true, Ordering::Acquire) {
            std::hint::spin_loop();
        }
    }
}
```

## Good
```rust
use std::sync::Mutex; // Backed by OS futex (futex syscall on Linux, WaitOnAddress on Windows)

pub struct SafeResource<T> {
    data: Mutex<T>,
}

impl<T> SafeResource<T> {
    pub fn access(&self) -> std::sync::MutexGuard<'_, T> {
        // OS puts thread to sleep if contended, freeing CPU cores for useful work
        self.data.lock().expect("mutex poisoned")
    }
}
```

## When Acceptable
Spinlocks are only valid in kernel development, real-time bare-metal embedded contexts without an OS scheduler, or bounded hybrid adaptive mutexes (e.g., `parking_lot::Mutex`) that spin briefly before sleeping.
