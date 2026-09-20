# er-typestate-pattern

> Encode lifecycle states into generic phantom types (Typestate Pattern) to make illegal transitions impossible at compile time.

## Why It Matters
Relying on runtime flags (e.g., `is_connected: bool`) requires defensive branching and runtime errors (`Err(NotConnected)`) in every method. In designs with a statically known lifecycle, the Typestate pattern shifts state transitions into type-level generic parameters, catching invalid protocol calls at compile time. Dynamic input validation and runtime state machines may still be necessary.

## Bad
```rust
pub struct Connection {
    connected: bool,
}

impl Connection {
    pub fn send(&self, msg: &[u8]) -> Result<(), &'static str> {
        // Runtime check required on every call!
        if !self.connected {
            return Err("not connected");
        }
        Ok(())
    }
}
```

## Good
```rust
use std::marker::PhantomData;

pub struct Disconnected;
pub struct Connected;

pub struct Connection<State> {
    _state: PhantomData<State>,
}

impl Connection<Disconnected> {
    pub fn connect(self) -> Connection<Connected> {
        Connection { _state: PhantomData }
    }
}

impl Connection<Connected> {
    // Not available on `Connection<Disconnected>` in this design.
    pub fn send(&self, _msg: &[u8]) {
        // Send payload safely
    }
}
```

## When Acceptable
Simple structs without distinct lifecycle stages or structures whose transitions depend on unpredictable dynamic user inputs where enum state machines are more appropriate.
