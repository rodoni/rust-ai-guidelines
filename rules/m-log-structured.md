# m-log-structured

> Emit telemetry events and spans with explicit key-value fields rather than formatted string interpolation.

## Why It Matters
Interpolating values directly into log message strings (`"User {} logged in from {}"`) makes reliable field extraction harder and may require parsing in log aggregators. Emitting key-value fields preserves event structure for filtering and querying; indexing still depends on the telemetry backend and its configuration.

## Bad
```rust
// Unstructured: Requires regex parsing in log aggregators
tracing::info!("User {} failed authentication from IP {}", user_id, ip_address);
```

## Good
```rust
// Structured: Indexed as distinct JSON/OpenTelemetry attributes
tracing::info!(
    user_id = %user_id,
    client_ip = %ip_address,
    attempt = attempt_count,
    "Authentication failed"
);
```

## See Also
- [m-log-not-print](m-log-not-print.md) - Telemetry instead of print statements
