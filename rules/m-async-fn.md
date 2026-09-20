# m-async-fn

> Prefer `async fn` syntax for ordinary asynchronous functions.

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
Use an explicit future type when recursion, trait object safety, MSRV compatibility, callback adaptation, combinator composition, or deliberate future boxing requires it. Document the allocation and lifetime trade-off when using `Pin<Box<dyn Future>>`.
