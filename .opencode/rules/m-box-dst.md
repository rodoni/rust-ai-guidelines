# m-box-dst

> Use `Box<[T]>` or `Box<str>` instead of `Vec<T>` or `String` for immutable owned sequences.

## Why It Matters
A `Vec<T>` and `String` carry 3 words (pointer, length, capacity = 24 bytes on 64-bit). Once built and immutable, `Box<[T]>` or `Box<str>` carries only 2 words (pointer, length = 16 bytes), saving 33% stack/struct footprint per instance.

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
