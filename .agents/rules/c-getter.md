# c-getter

> Omit the `get_` prefix on standard getter methods.

## Why It Matters
In idiomatic Rust, getters match the property name directly. The `get` prefix is reserved exclusively for methods that can fail or return an option/sub-slice (e.g. `HashMap::get`, `slice::get`).

## Bad
```rust
struct Connection {
    port: u16,
    host: String,
}

impl Connection {
    fn get_port(&self) -> u16 { self.port }
    fn get_host(&self) -> &str { &self.host }
}
```

## Good
```rust
impl Connection {
    fn port(&self) -> u16 { self.port }
    fn host(&self) -> &str { &self.host }
    
    // Mutable getter follows _mut
    fn host_mut(&mut self) -> &mut String { &mut self.host }
}
```

## When Acceptable
Use `get` when lookup might fail:
```rust
impl KeyRing {
    // Legitimate 'get': returns Option because key may not exist
    fn get(&self, id: KeyId) -> Option<&Key> { ... }
}
```
