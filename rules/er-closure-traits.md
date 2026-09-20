# er-closure-traits

> Accept the least restrictive closure trait in public APIs (`Fn` > `FnMut` > `FnOnce`) based on call frequency.

## Why It Matters
A closure implementing `Fn` can also satisfy `FnMut` and `FnOnce`, but the reverse is not true. Requiring `Fn` when the function is only invoked once artificially excludes closures that capture state by unique reference (`&mut`) or by value. Conversely, taking `FnOnce` when called in a loop fails to compile.

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
