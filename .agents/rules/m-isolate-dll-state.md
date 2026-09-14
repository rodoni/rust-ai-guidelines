# m-isolate-dll-state

> Isolate global runtime state when exposing Rust libraries as dynamic libraries (DLLs/so/dylib).

## Why It Matters
When multiple host applications or plugins load a shared dynamic library, global statics or threads started in one instance can collide, corrupt memory, or cause deadlocks upon library unloading.

## Bad
```rust
// Global mutable static shared across all host loaders
static mut GLOBAL_SESSION: Option<Session> = None;

#[no_mangle]
pub extern "C" fn init_session() {
    unsafe { GLOBAL_SESSION = Some(Session::new()); }
}
```

## Good
```rust
// Return an opaque instance handle to the host caller
pub struct OpaqueSession(Session);

#[no_mangle]
pub extern "C" fn session_create() -> *mut OpaqueSession {
    let session = Box::new(OpaqueSession(Session::new()));
    Box::into_raw(session)
}

#[no_mangle]
pub unsafe extern "C" fn session_destroy(ptr: *mut OpaqueSession) {
    if !ptr.is_null() {
        // SAFETY: ptr was created by session_create via Box::into_raw
        drop(unsafe { Box::from_raw(ptr) });
    }
}
```
