# m-avoid-wrappers

> Do not expose smart pointers (`Arc`, `Rc`, `Mutex`, `Box`) in public API signatures.

## Why It Matters
Forcing `Arc<T>` or `Mutex<T>` in parameter or return types locks callers into a specific synchronization or allocation strategy. Keep them internal to structs.

## Bad
```rust
// Forces caller to use Arc and Mutex even in single-threaded tests
pub fn process_event(client: Arc<Mutex<Client>>, payload: &[u8]) {}

// Leaks heap allocation requirement
pub fn make_handler() -> Box<dyn Handler> {}
```

## Good
```rust
// Caller passes regular reference; Client internally handles locking if needed
pub fn process_event(client: &Client, payload: &[u8]) {}

// Impl Trait hides allocation decision from public contract
pub fn make_handler() -> impl Handler {}
```

## When Acceptable
When a type is designed explicitly to manage shared ownership across threads and has internal state wrapped inside (e.g. `Client { inner: Arc<Inner> }`).
