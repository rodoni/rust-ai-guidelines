# sync-avoid-spinlock

> Avoid unbounded busy-wait spinlocks in general-purpose user space; prefer blocking or bounded adaptive synchronization.

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
use std::sync::Mutex; // Platform-backed blocking synchronization

pub struct SafeResource<T> {
    data: Mutex<T>,
}

impl<T> SafeResource<T> {
    pub fn access(&self) -> std::sync::MutexGuard<'_, T> {
        // The platform implementation can block instead of busy-waiting.
        self.data.lock().expect("mutex poisoned")
    }
}
```

## When Acceptable
Short, bounded spinning can be valid for carefully measured, extremely short critical sections or specialized runtimes. Unbounded spinning is generally inappropriate in preemptive user-space programs; blocking locks, parking, or adaptive primitives are safer defaults.
