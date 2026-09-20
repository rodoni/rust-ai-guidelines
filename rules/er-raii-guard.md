# er-raii-guard

> Encapsulate state cleanup and resource release into RAII guard types with `Drop` implementations.

## Why It Matters
Manually resetting flags, closing handles, or unlocking resources before returning is fragile. An early return via `?`, a panic during stack unwinding, or an unhandled branch skips manual cleanup, leaking resources or leaving data structures in poisoned states. RAII guards perform cleanup on normal scope exit and during unwinding; they do not run after process aborts, `process::exit`, or deliberate leaks.

## Bad
```rust
pub struct Session {
    pub is_active: bool,
}

pub fn process_session(session: &mut Session) -> Result<(), &'static str> {
    session.is_active = true;

    // HAZARD: Early return leaves `is_active == true` permanently!
    risky_operation()?;

    session.is_active = false;
    Ok(())
}
```

## Good
```rust
pub struct Session {
    is_active: bool,
}

// RAII guard holds a mutable borrow and guarantees reset on drop
pub struct ActiveSessionGuard<'a>(&'a mut Session);

impl<'a> Session {
    pub fn enter(&'a mut self) -> ActiveSessionGuard<'a> {
        self.is_active = true;
        ActiveSessionGuard(self)
    }
}

impl<'a> Drop for ActiveSessionGuard<'a> {
    fn drop(&mut self) {
        self.0.is_active = false;
    }
}

pub fn process_session(session: &mut Session) -> Result<(), &'static str> {
    let _guard = session.enter();
    risky_operation()?; // If this fails or panics, `_guard` drops and resets state!
    Ok(())
}
```

## When Acceptable
Simple POD (Plain Old Data) structures that do not manage external resources, handles, or invariants requiring post-execution restoration.
