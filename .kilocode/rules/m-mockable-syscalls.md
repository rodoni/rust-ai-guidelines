# m-mockable-syscalls

> Design core domain logic "sans I/O" or abstract system calls behind mockable traits.

## Why It Matters
Direct hardcoded invocations of `std::fs`, `tokio::net`, or system time prevent deterministic fast unit testing, forcing tests to rely on real file systems or flaky network sockets.

## Bad
```rust
pub struct OrderProcessor;

impl OrderProcessor {
    pub async fn process(&self, order: Order) -> Result<()> {
        // Hardcoded real disk I/O and real network calls!
        tokio::fs::write("orders.txt", order.serialize()).await?;
        reqwest::Client::new().post("https://payment.com").send().await?;
        Ok(())
    }
}
```

## Good
```rust
// Core logic takes abstract traits or pure data ("sans I/O")
pub trait PaymentGateway {
    async fn charge(&self, amount: u64) -> Result<(), PaymentError>;
}

pub struct OrderProcessor<P: PaymentGateway> {
    payment: P,
}

// In unit tests: instant mock without hitting the real network
```
