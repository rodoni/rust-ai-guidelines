# m-init-builder

> Use the Builder pattern for structs with complex or optional configuration.

## Why It Matters
Structs with more than 3-4 fields become unwieldy to construct and cause breaking API changes whenever a new field is added. The final `.build()` method should validate invariants fallibly.

## Bad
```rust
// Adding a field here breaks all callers!
pub struct HttpClient {
    pub timeout: Duration,
    pub retries: u32,
    pub base_url: String,
}
```

## Good
```rust
pub struct HttpClient {
    timeout: Duration,
    retries: u32,
    base_url: String,
}

pub struct HttpClientBuilder {
    timeout: Option<Duration>,
    retries: Option<u32>,
    base_url: Option<String>,
}

impl HttpClientBuilder {
    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = Some(timeout);
        self
    }
    
    pub fn build(self) -> Result<HttpClient, ConfigError> {
        let base_url = self.base_url.ok_or(ConfigError::MissingBaseUrl)?;
        Ok(HttpClient {
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
            retries: self.retries.unwrap_or(3),
            base_url,
        })
    }
}
```
