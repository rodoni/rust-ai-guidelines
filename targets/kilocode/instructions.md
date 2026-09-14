# Kilo Code Custom Rules & Instructions

Guidelines for Kilo Code and compatible editor AI agents.

## Core Directives
1. **Low-Context Loading**: Reference `rules/<rule-id>.md` only on demand. Do not dump extensive documentation into user chat.
2. **Standard Traits**: Always derive `Debug`, `Clone`, `Default`, `Eq`, `Hash` where sound.
3. **Sound Boundaries**: No `unsafe` without an explicit `// SAFETY:` explanation.
4. **Error Handling**: Use canonical typed enums with `thiserror` for libraries, `anyhow` only for top-level binaries.
5. **Memory**: Preallocate capacity (`with_capacity`) and reuse buffers with `.clear()`.
