# c-getter

> Omit the `get_` prefix on standard getter methods.

## Why It Matters
In idiomatic Rust, simple property getters match the property name directly. `get` is also idiomatic for lookup-style methods and other APIs whose naming or compatibility benefits from the prefix; it is not reserved exclusively for fallible or optional results.

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
