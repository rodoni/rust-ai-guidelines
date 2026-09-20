# c-send-sync

> Ensure public types are `Send` and `Sync` whenever thread safety is sound.

## Why It Matters
Types used in async runtimes or multi-threaded architectures may need `Send` and/or `Sync` depending on how they are moved or shared. For example, a spawned Tokio future generally needs `Send + 'static`; `Sync` is required when shared references cross threads. A single non-Send field can prevent movement across threads.

## Bad
```rust
use std::rc::Rc;

// Non-Send because of Rc, cannot be passed across threads or tasks!
pub struct ServiceContext {
    config: Rc<AppConfig>,
}
```

## Good
```rust
use std::sync::Arc;

// `Arc<T>` is Send + Sync only when `T` is Send + Sync.
pub struct ServiceContext {
    config: Arc<AppConfig>,
}

// Compile-time assertion in library tests
#[test]
fn assert_send_sync() {
    fn assert_traits<T: Send + Sync>() {}
    assert_traits::<ServiceContext>();
}
```

## When Acceptable
Single-threaded GUI event loops or explicit thread-local caches may deliberately omit `Send` or `Sync`.
