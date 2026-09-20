# m-avoid-wrappers

> Do not expose implementation-detail smart pointers in public API signatures.

## Why It Matters
Forcing `Arc<T>` or `Mutex<T>` in parameter or return types locks callers into a specific synchronization or allocation strategy. Keep them internal to structs unless ownership, dynamic dispatch, recursion, or an ABI explicitly requires an exposed wrapper.

## Bad
```rust
// Forces caller to use Arc and Mutex even in single-threaded tests
pub fn process_event(client: Arc<Mutex<Client>>, payload: &[u8]) {}

// Exposes a heap allocation when dynamic dispatch is not required
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
When a type is designed explicitly to manage shared ownership across threads, or when `Box<dyn Trait>`/`Pin<Box<dyn Future>>` is required for heterogeneous values, recursion, object safety, or ABI compatibility.
