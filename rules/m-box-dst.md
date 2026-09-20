# m-box-dst

> Consider `Box<[T]>` or `Box<str>` for frequently instantiated, immutable internal sequences when measurement justifies the smaller handle.

## Why It Matters
On common 64-bit targets, a `Vec<T>` or `String` carries 3 words while a boxed slice or string carries 2 words. This can reduce the handle size for frequently instantiated internal values, but adds an allocation and may not benefit public APIs or small collections.

## Bad
```rust
// 24 bytes per struct field
pub struct Header {
    pub name: String,
    pub values: Vec<String>,
}
```

## Good
```rust
// 16 bytes per struct field
pub struct Header {
    pub name: Box<str>,
    pub values: Box<[Box<str>]>,
}

// Easy conversion using into_boxed_slice / into_boxed_str
let values: Box<[Box<str>]> = raw_vec.into_iter().map(|s| s.into_boxed_str()).collect();
```
