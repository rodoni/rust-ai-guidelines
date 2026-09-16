# c-deref

> Implement `Deref` and `DerefMut` strictly for smart pointer types, never to simulate OOP inheritance.

## Why It Matters
`Deref` coercion is meant exclusively for smart pointers (`Box`, `Arc`, `Rc`, custom pointers). Abusing `Deref` to expose inner struct fields or simulate class inheritance causes confusing method resolution, breaks generic trait matching, and produces fragile, unexpected API behavior.

## Bad
```rust
pub struct User {
    pub name: String,
}

pub struct AdminUser {
    user: User,
    role: String,
}

// Anti-pattern: using Deref to simulate inheritance!
impl std::ops::Deref for AdminUser {
    type Target = User;
    fn deref(&self) -> &Self::Target {
        &self.user
    }
}
```

## Good
```rust
pub struct User {
    pub name: String,
}

pub struct AdminUser {
    user: User,
    role: String,
}

impl AdminUser {
    // Explicit accessor methods or composition
    pub fn user(&self) -> &User {
        &self.user
    }

    pub fn role(&self) -> &str {
        &self.role
    }
}
```

## See Also
- [c-smart-ptr](c-smart-ptr.md) - Smart pointers do not add inherent methods
- [c-getter](c-getter.md) - Getter naming conventions
