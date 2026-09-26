# er-closure-traits

> Accept the least restrictive closure trait required by the call pattern: prefer `FnOnce` over `FnMut`, and `FnMut` over `Fn`.

## Why It Matters
In Rust's closure traits hierarchy (and Effective Rust Item 10 standard traits), closures follow a strict subtyping relationship: every closure implementing `Fn` also implements `FnMut` and `FnOnce`, but the reverse is not true. Requiring `Fn` when `FnOnce` suffices artificially blocks closures that take ownership of captured variables. Use `FnOnce` for one-shot execution, `FnMut` for stateful loops, and `Fn` only when repeated concurrent or non-mutating access is required.

## Bad
```rust
// Over-restricts: forces callers to provide Fn even though the closure is only invoked once!
pub fn run_once<F>(action: F)
where
    F: Fn(),
{
    action();
}

// Cannot pass a closure that moves an owned value into action!
```

## Good
```rust
// Rule:
// 1. Invoked once: use FnOnce
pub fn run_once<F>(action: F)
where
    F: FnOnce(),
{
    action();
}

// 2. Invoked multiple times, mutates state: use FnMut
pub fn retry_loop<F>(mut step: F)
where
    F: FnMut() -> bool,
{
    while !step() {}
}

// 3. Invoked concurrently across threads: use Fn + Send + Sync
pub fn spawn_workers<F>(work: F)
where
    F: Fn() + Send + Sync + 'static,
{
    // ...
}
```

## When Acceptable
When an API explicitly requires concurrent, non-mutating invocations across threads, `Fn + Sync` is required.
