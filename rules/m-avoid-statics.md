# m-avoid-statics

> Avoid mutable or complex global state; pass state explicitly or via dependency injection.

## Why It Matters
Mutable globals, process-wide caches, and singletons create hidden coupling between components, make unit tests nondeterministic and order-dependent when run in parallel, and complicate initialization order. Immutable constants and immutable data initialized once with a documented lifetime (for example, `OnceLock<T>`) can be appropriate when dependency injection is impractical.

## Bad
```rust
use std::sync::Mutex;

// Global mutable state: impairs testing and causes race conditions
static GLOBAL_CACHE: Mutex<Option<DatabaseCache>> = Mutex::new(None);

pub fn get_user(id: u64) -> Option<User> {
    GLOBAL_CACHE.lock().unwrap().as_ref()?.lookup(id)
}
```

## Good
```rust
// Explicit instance passed via dependency injection or service struct
pub struct UserService {
    cache: DatabaseCache,
}

impl UserService {
    pub fn new(cache: DatabaseCache) -> Self {
        Self { cache }
    }

    pub fn get_user(&self, id: u64) -> Option<User> {
        self.cache.lookup(id)
    }
}
```

## See Also
- [m-services-clone](m-services-clone.md) - Service structs with cheap Clone
- [m-mockable-syscalls](m-mockable-syscalls.md) - Mockable system dependencies
