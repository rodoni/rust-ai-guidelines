# m-services-clone

> Make service and client handle structs cheaply `Clone` using internal shared state.

## Why It Matters
In async frameworks (Axum, Actix, Tonic), services and client handles are frequently cloned per request or spawned task. If cloning is cheap (wrapping an `Arc<Inner>`), ergonomically handing off state is trivial.

## Bad
```rust
// Heavy struct: cloning clones sockets, buffers, and caches
#[derive(Clone)]
pub struct ApiClient {
    cache: HashMap<String, String>,
    endpoints: Vec<String>,
}
```

## Good
```rust
// Cheap handle: cloning just increments an Arc atomic counter
#[derive(Clone)]
pub struct ApiClient {
    inner: std::sync::Arc<ApiClientInner>,
}

struct ApiClientInner {
    cache: tokio::sync::RwLock<HashMap<String, String>>,
    endpoints: Vec<String>,
}
```
