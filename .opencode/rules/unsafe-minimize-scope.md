# unsafe-minimize-scope

> Keep `unsafe` blocks as small as possible; never wrap safe operations inside `unsafe`.

## Why It Matters
Wrapping multiple lines or entire functions in `unsafe` obscures which exact operation triggers the need for unsafety and turns off safety scrutiny for ordinary code within that block.

## Bad
```rust
unsafe {
    let raw = get_ptr();
    let val = *raw; // Only this dereference is unsafe!
    println!("Val is: {val}");
    notify_listener(val);
}
```

## Good
```rust
let raw = get_ptr();

// SAFETY: `raw` is valid for reads and properly aligned.
let val = unsafe { *raw };

println!("Val is: {val}");
notify_listener(val);
```
