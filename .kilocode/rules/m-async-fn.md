# m-async-fn

> Use `async fn` syntax instead of manually returning `impl Future`.

## Why It Matters
Native `async fn` is cleaner, properly preserves lifetime elision, and allows compiler tooling to optimize the generated state machine.

## Bad
```rust
// Verbose and can cause tricky lifetime capture issues
pub fn fetch_data<'a>(&'a self, id: &'a str) -> impl std::future::Future<Output = Result<Data>> + 'a {
    async move { ... }
}
```

## Good
```rust
// Clear, idiomatic, auto-captures &self correctly
pub async fn fetch_data(&self, id: &str) -> Result<Data> {
    ...
}
```

## When Acceptable
Only return explicit `Pin<Box<dyn Future>>` when recursive async functions are required or trait object safety without AFIT is needed.
