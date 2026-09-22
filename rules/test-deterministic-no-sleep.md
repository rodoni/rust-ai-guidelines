# test-deterministic-no-sleep

> Eliminate wall-clock sleeps (`std::thread::sleep`) in unit tests; use simulated clocks or `tokio::time::pause()`.

## Why It Matters
Using `thread::sleep` or `tokio::time::sleep` with real wall-clock durations causes slow CI pipelines and flaky test suites. Under variable CI CPU loads, arbitrary delays (e.g. `sleep(100ms)`) often expire prematurely or lag behind schedule, causing non-deterministic race conditions and random failures.

## Bad
```rust
#[tokio::test]
async fn test_rate_limiter_reset() {
    let limiter = RateLimiter::new(1, Duration::from_millis(50));
    limiter.acquire().await.unwrap();

    // BAD: Real wall-clock sleep; burns CPU time and creates flaky tests under CI load
    tokio::time::sleep(Duration::from_millis(60)).await;

    assert!(limiter.try_acquire());
}
```

## Good
```rust
#[tokio::test(start_paused = true)]
async fn test_rate_limiter_reset() {
    let limiter = RateLimiter::new(1, Duration::from_secs(60));
    limiter.acquire().await.unwrap();

    // GOOD: Instantly advances virtual time by 60 seconds deterministically
    tokio::time::advance(Duration::from_secs(60)).await;

    assert!(limiter.try_acquire());
}
```

## When Acceptable
Long-running end-to-end integration or soak tests specifically measuring actual operating system timer precision and hardware clock drift.
