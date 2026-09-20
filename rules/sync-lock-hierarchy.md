# sync-lock-hierarchy

> Enforce a strict, documented acquisition order when acquiring multiple locks to prevent deadlocks.

## Why It Matters
When two threads acquire the same set of locks in opposing order (Thread A locks L1 then L2; Thread B locks L2 then L1), a cyclic dependency creates an irrecoverable deadlock. Establishing a total order (by memory address, domain ID, or dedicated guard) mathematically prevents circular wait conditions.

## Bad
```rust
use std::sync::Mutex;

struct Account {
    balance: Mutex<u64>,
}

#[derive(Debug)]
enum TransferError {
    SameAccount,
    NonUniqueAccountIds,
}

fn transfer(from: &Account, to: &Account, amount: u64) -> Result<(), TransferError> {
    if std::ptr::eq(from, to) {
        return Err(TransferError::SameAccount);
    }
    if from.id == to.id {
        return Err(TransferError::NonUniqueAccountIds);
    }

    // DEADLOCK HAZARD: If two threads transfer between each other simultaneously!
    let mut f = from.balance.lock().unwrap();
    let mut t = to.balance.lock().unwrap();
    *f -= amount;
    *t += amount;
    Ok(())
}
```

The ordering key must be unique for every lock participating in the protocol. Reject
self-transfers and duplicate keys before acquiring either lock.

## Good
```rust
use std::sync::Mutex;

struct Account {
    id: u64,
    balance: Mutex<u64>,
}

fn transfer(from: &Account, to: &Account, amount: u64) {
    // Acquire locks in deterministic ascending ID order
    let (first, second) = if from.id < to.id {
        (&from.balance, &to.balance)
    } else {
        (&to.balance, &from.balance)
    };

    let mut lock1 = first.lock().unwrap();
    let mut lock2 = second.lock().unwrap();

    let (mut f, mut t) = if from.id < to.id {
        (lock1, lock2)
    } else {
        (lock2, lock1)
    };

    *f -= amount;
    *t += amount;
}
```

## When Acceptable
Systems utilizing lock-free data structures, actor message passing, or channel-based synchronization (`mpsc`/`crossbeam`) that avoid multi-lock acquisition altogether.
