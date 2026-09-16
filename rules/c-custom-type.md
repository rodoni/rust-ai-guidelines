# c-custom-type

> Convey meaning through dedicated domain types and enums rather than primitive flags (`bool`) or ambiguous `Option`.

## Why It Matters
Boolean flags at call sites (`process(true, false)`) are cryptic, error-prone, and hide domain intent. AI coding assistants frequently swap adjacent boolean arguments. Domain enums make the intent self-documenting at the call site.

## Bad
```rust
// Cryptic call site: what do true and false mean?
pub fn search_documents(query: &str, include_archived: bool, case_sensitive: bool) {
    // ...
}

// Call site is completely opaque:
search_documents("report", true, false);
```

## Good
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum ArchiveFilter {
    #[default]
    ActiveOnly,
    IncludeArchived,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum CaseSensitivity {
    #[default]
    Insensitive,
    Sensitive,
}

pub fn search_documents(
    query: &str,
    archive: ArchiveFilter,
    case: CaseSensitivity,
) {
    // ...
}

// Call site is self-documenting and impossible to swap:
search_documents("report", ArchiveFilter::IncludeArchived, CaseSensitivity::Insensitive);
```

## See Also
- [c-newtype](c-newtype.md) - Use Newtypes for primitive distinction
- [m-design-for-ai](m-design-for-ai.md) - Design types for AI comprehension
