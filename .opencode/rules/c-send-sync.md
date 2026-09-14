# c-send-sync

> Ensure public types are `Send` and `Sync` whenever thread safety is sound.

## Why It Matters
Types used in async runtimes (Tokio, async-std) or multi-threaded architectures require `Send + Sync` to cross task boundaries (`tokio::spawn`). A single non-Send field breaks concurrency downstream.

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

// Thread-safe: implements Send + Sync automatically
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
