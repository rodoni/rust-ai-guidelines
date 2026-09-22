# test-fakes-over-heavy-mocks

> Favor in-memory fakes and thin traits over complex dynamic mocking frameworks with lifetimes.

## Why It Matters
Dynamic mocking frameworks often require heavy macro attributes, enforce rigid `'static` lifetime bounds, and tie tests to exact call sequences rather than business outcomes. In-memory fakes (e.g. `HashMap`-backed stores or channel-based queues) provide robust, reusable, and type-safe test environments that execute at full native speed.

## Bad
```rust
// Heavy mocking framework with brittle exact-call expectations
#[test]
fn test_order_creation() {
    let mut mock = MockDatabase::new();
    mock.expect_get_user()
        .with(mockall::predicate::eq(123))
        .times(1)
        .returning(|_| Ok(User::active(123)));
    mock.expect_save_order()
        .times(1)
        .returning(|_| Ok(()));

    let service = OrderService::new(mock);
    service.create_order(123, 50).unwrap();
}
```

## Good
```rust
// Simple, reusable in-memory fake without lifetime or macro friction
#[derive(Default)]
struct InMemoryDatabase {
    users: std::sync::Mutex<std::collections::HashMap<u64, User>>,
    orders: std::sync::Mutex<Vec<Order>>,
}

impl Database for InMemoryDatabase {
    fn get_user(&self, id: u64) -> Result<User, DbError> {
        self.users.lock().unwrap().get(&id).cloned().ok_or(DbError::NotFound)
    }
    fn save_order(&self, order: Order) -> Result<(), DbError> {
        self.orders.lock().unwrap().push(order);
        Ok(())
    }
}

#[test]
fn test_order_creation() {
    let db = InMemoryDatabase::default();
    db.users.lock().unwrap().insert(123, User::active(123));

    let service = OrderService::new(db);
    service.create_order(123, 50).unwrap();
}
```

## When Acceptable
Third-party clients or protocol drivers with vast, sprawling trait surfaces where writing an in-memory fake requires implementing dozens of unused methods.
