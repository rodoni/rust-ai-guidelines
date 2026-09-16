# Rust AI Guidelines & Agentic Tools

Conjunto modular de **Agentes de IA**, **SKILLS** e **Regras Atômicas** otimizados para desenvolvimento agêntico em Rust com **foco em baixíssimo consumo de contexto** (*Zero Token Waste*).

---

## 💎 Filosofia: Curadoria de Alto Impacto (*Curated Core*)

Tanto o [Official Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) (55 itens) quanto o [Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/) (89 itens) totalizam **mais de 140 diretrizes**.

Diferente de abordagens ingênuas que despejam livros inteiros na janela de contexto das LLMs — desperdiçando dezenas de milhares de tokens e gerando alucinações —, este ecossistema destila **as 54 regras mais críticas e fundamentais**:
1. **Segurança e Soundness Inegociáveis**: Zero tolerância para `unsafe` sem `// SAFETY:`, prevenção estrita de *Undefined Behavior*, destrutores sem pânico e sound C-ABI FFI.
2. **Eficiência de Memória e Compilação**: Pré-alocação cirúrgica, reaproveitamento de buffers (`.clear()`), `Box<[T]>`, mimalloc e limites rígidos de stack assíncrono.
3. **Ergonomia e Robustez de APIs**: Newtypes contra obsessão primitiva, eliminação de vazamento de smart pointers (`Arc`/`Mutex`), traits idiomáticos (`From`, `AsRef`) e semver selado.
4. **Resiliência e Observabilidade Corporativa**: Telemetria estruturada (`tracing`), ausência de `println!` em produção, features estritamente aditivas e `[workspace.dependencies]` centralizado.

> ⚡ **Zero Token Waste**: Cada regra é atômica (30 a 60 linhas), auto-contida e carregada **sob demanda** pelos agentes especializados.

---

## 🎯 Compatibilidade Multi-Ambiente

Projetado para funcionar de forma nativa e sem fricção em múltiplos ambientes:
- **Google Antigravity** (`.agents/skills/`, `.agents/rules/`, `.agents/agents/` e `.agents/AGENTS.md`)
- **OpenCode / OpenCodeInterpreter** (`.opencode/rules/`, `.opencode/skills/`, `.opencode/agents/` e `.opencode/AGENTS.md`)
- **Kilo Code** (`.kilo/` e `kilo.jsonc`)
- **Cursor** (`.cursor/rules/*.mdc`, `.cursor/skills/` e `.cursor/agents/`)
- **Claude Code** (`.claude/` e `CLAUDE.md`)
- **GitHub Copilot** (`.github/copilot-instructions.md`)

> 🛡️ **Instalação Não-Invasiva**: Nenhuma configuração destrutiva sobrescreve arquivos existentes na raiz do projeto. Todo o ecossistema é confinado nas pastas das respectivas ferramentas.

---

## 🧠 Agentes Especializados (`agents/`)

Em vez de sobrecarregar um único prompt genérico com dezenas de milhares de tokens, o trabalho é dividido entre agentes com escopos precisos:

| Agente | Arquivo | Responsabilidade |
|---|---|---|
| **`rust-lead`** | [`agents/rust-lead.md`](agents/rust-lead.md) | Orquestração, planejamento modular e triagem de tarefas. |
| **`rust-api-architect`** | [`agents/rust-api-architect.md`](agents/rust-api-architect.md) | Design de APIs públicas, convenções RFC 430, builders, Newtypes e traits. |
| **`rust-perf-optimizer`** | [`agents/rust-perf-optimizer.md`](agents/rust-perf-optimizer.md) | Otimização de memória, pré-alocação, buffers, hashers rápidos e async stack. |
| **`rust-safety-auditor`** | [`agents/rust-safety-auditor.md`](agents/rust-safety-auditor.md) | Auditoria de `unsafe`, comentários `// SAFETY:`, sound boundaries e invariantes. |
| **`rust-reviewer`** | [`agents/rust-reviewer.md`](agents/rust-reviewer.md) | Revisão ágil de código, lints com `#[expect]`, dead code e conformidade. |

### 📊 Matriz de Mapeamento: Agentes ➔ Skills ➔ Regras

| Agente | Skill Primária | Skills Secundárias | Regras Atômicas Enforced (`rules/*.md`) |
|---|---|---|---|
| **`rust-lead`** | [`rust-guidelines`](skills/rust-guidelines/SKILL.md) *(Master Hub)* | Todas as 6 skills temáticas | `m-cargo-workspace`, `m-smaller-crates`, `m-mockable-syscalls`, `m-design-for-ai` |
| **`rust-api-architect`** | [`rust-api`](skills/rust-api/SKILL.md) *(API & Ergonomia)* | `rust-resilience-app`, `rust-macros` | `c-case`, `c-conv`, `c-getter`, `c-common-traits`, `c-send-sync`, `c-newtype`, `c-sealed`, `c-conv-traits`, `c-custom-type`, `c-deref`, `c-generic`, `c-smart-ptr`, `m-weasel-words`, `m-regular-fn`, `m-avoid-wrappers`, `m-dont-leak-types`, `m-di-hierarchy`, `m-init-builder`, `m-services-clone`, `m-async-fn`, `m-macro-last-resort`, `m-example-over-proc`, `m-proc-impl`, `m-macro-helpers` |
| **`rust-perf-optimizer`** | [`rust-perf`](skills/rust-perf/SKILL.md) *(Memória & Async)* | `rust-api`, `rust-resilience-app` | `mem-with-capacity`, `mem-reuse-collections`, `m-box-dst`, `m-shrink-to-fit`, `m-fast-hasher`, `m-async-stack-size`, `m-yield-points`, `m-mimalloc-apps` |
| **`rust-safety-auditor`** | [`rust-safety`](skills/rust-safety/SKILL.md) *(Soundness & Erros)* | [`rust-ffi`](skills/rust-ffi/SKILL.md), `rust-api` | `unsafe-safety-comment`, `unsafe-minimize-scope`, `m-unsound-prevention`, `m-panic-on-bug`, `m-errors-canonical`, `c-dtor-fail`, `m-avoid-statics`, `m-strong-types-guard`, `m-ffi-translates`, `m-isolate-dll-state`, `m-ffi-naming` |
| **`rust-reviewer`** | [`rust-resilience-app`](skills/rust-resilience-app/SKILL.md) *(Lints & Contratos)* | `rust-safety`, `rust-api`, `rust-perf` | `m-lint-override-expect`, `c-failure`, `m-macro-helpers`, `m-test-util`, `m-app-error`, `m-design-for-ai`, `m-log-not-print`, `m-log-structured`, `m-features-additive` |


---

## 📦 SKILLS Modulares (`skills/`)

As diretrizes são organizadas em skills temáticas carregadas sob demanda:

1. **[`rust-guidelines`](skills/rust-guidelines/SKILL.md)**: Hub mestre com tabela de roteamento e links para todas as regras.
2. **[`rust-api`](skills/rust-api/SKILL.md)**: Convenções de nomenclatura, interoperabilidade de traits, Newtypes, builders e ergonomia.
3. **[`rust-perf`](skills/rust-perf/SKILL.md)**: `with_capacity`, reaproveitamento de buffers com `.clear()`, `Box<[T]>`, mimalloc e limites de stack assíncrono.
4. **[`rust-safety`](skills/rust-safety/SKILL.md)**: Comentários obrigatórios `// SAFETY:`, escopo cirúrgico de `unsafe`, sound FFI e filosofia de Pânico vs Result.
5. **[`rust-macros`](skills/rust-macros/SKILL.md)**: Macros declarativas antes de procedurais, crates de implementação separadas e exportação `_private`.
6. **[`rust-ffi`](skills/rust-ffi/SKILL.md)**: Isolamento de estado DLL, ponte FFI pura sem regra de negócio acoplada e C-ABI naming.
7. **[`rust-resilience-app`](skills/rust-resilience-app/SKILL.md)**: Arquitetura "sans I/O" (syscalls mockáveis), `test-util` feature gate e contratos de documentação para IA.

---

## ⚡ Regras Atômicas de Baixo Contexto (`rules/`)

Cada regra em [`rules/`](rules/) possui entre 30 e 60 linhas e segue a estrutura padronizada:
- **Imperativo de 1 linha**: Orientação imediata.
- **Why It Matters**: 1 a 2 sentenças técnicas explicando o impacto.
- **Bad**: Snippet curto demonstrando o antipadrão.
- **Good**: Snippet corrigido, idiomático e com zero desperdício de memória ou CPU.
- **When Acceptable / See Also**: Casos válidos de exceção e links correlatos.

### 📋 Catálogo Completo das 54 Regras Atômicas

Tabela consolidada de todas as **54 regras essenciais** implementadas no ecossistema:

| Categoria | Regra | Origem | Diretriz Atômica |
|---|---|---|---|
| **Segurança & Soundness** | [`c-dtor-fail`](rules/c-dtor-fail.md) | Rust API Guidelines | Destructors (`Drop` trait implementations) must never panic or fail. |
| **Segurança & Soundness** | [`m-avoid-statics`](rules/m-avoid-statics.md) | Microsoft Pragmatic Rust | Avoid mutable or complex global statics; pass state explicitly or via dependency injection. |
| **Segurança & Soundness** | [`m-errors-canonical`](rules/m-errors-canonical.md) | Microsoft Pragmatic Rust | Library error types must be strongly typed canonical enums using `thiserror`. |
| **Segurança & Soundness** | [`m-panic-on-bug`](rules/m-panic-on-bug.md) | Microsoft Pragmatic Rust | Panics are exclusively for impossible invariants and programming bugs; use `Result` for runtime failures. |
| **Segurança & Soundness** | [`m-strong-types-guard`](rules/m-strong-types-guard.md) | Microsoft Pragmatic Rust | Enforce domain invariants upon type construction (*Parse, Don't Validate*). |
| **Segurança & Soundness** | [`m-unsound-prevention`](rules/m-unsound-prevention.md) | Microsoft Pragmatic Rust | Public safe APIs wrapping `unsafe` internals must be 100% sound under all possible inputs. |
| **Segurança & Soundness** | [`unsafe-minimize-scope`](rules/unsafe-minimize-scope.md) | Pragmatic / Soundness | Keep `unsafe` blocks as small as possible; never wrap safe operations inside `unsafe`. |
| **Segurança & Soundness** | [`unsafe-safety-comment`](rules/unsafe-safety-comment.md) | Pragmatic / Soundness | Every `unsafe` block must have an explicit `// SAFETY:` comment justifying why it is sound. |
| **API & Ergonomia** | [`c-case`](rules/c-case.md) | Rust API Guidelines | Follow RFC 430 casing conventions strictly. |
| **API & Ergonomia** | [`c-common-traits`](rules/c-common-traits.md) | Rust API Guidelines | Eagerly implement or derive standard library traits on public types. |
| **API & Ergonomia** | [`c-conv`](rules/c-conv.md) | Rust API Guidelines | Name ad-hoc conversions following `as_`, `to_`, and `into_` conventions. |
| **API & Ergonomia** | [`c-conv-traits`](rules/c-conv-traits.md) | Rust API Guidelines | Implement standard conversion traits (`From`, `TryFrom`, `AsRef`, `AsMut`) instead of bespoke ad-hoc methods. |
| **API & Ergonomia** | [`c-custom-type`](rules/c-custom-type.md) | Rust API Guidelines | Convey meaning through dedicated domain types and enums rather than primitive flags (`bool`) or ambiguous `Option`. |
| **API & Ergonomia** | [`c-deref`](rules/c-deref.md) | Rust API Guidelines | Implement `Deref` and `DerefMut` strictly for smart pointer types, never to simulate OOP inheritance. |
| **API & Ergonomia** | [`c-generic`](rules/c-generic.md) | Rust API Guidelines | Minimize assumptions about function parameters by taking flexible generic bounds (`AsRef`, `Into`, `Borrow`). |
| **API & Ergonomia** | [`c-getter`](rules/c-getter.md) | Rust API Guidelines | Omit the `get_` prefix on standard getter methods. |
| **API & Ergonomia** | [`c-newtype`](rules/c-newtype.md) | Rust API Guidelines | Use Newtypes to enforce semantic distinctions and encapsulate validation. |
| **API & Ergonomia** | [`c-sealed`](rules/c-sealed.md) | Rust API Guidelines | Use the sealed trait pattern to prevent downstream external implementations. |
| **API & Ergonomia** | [`c-send-sync`](rules/c-send-sync.md) | Rust API Guidelines | Ensure public types are `Send` and `Sync` whenever thread safety is sound. |
| **API & Ergonomia** | [`c-smart-ptr`](rules/c-smart-ptr.md) | Rust API Guidelines | Smart pointers do not add inherent methods to avoid method resolution collisions with dereferenced targets. |
| **API & Ergonomia** | [`m-async-fn`](rules/m-async-fn.md) | Microsoft Pragmatic Rust | Use `async fn` syntax instead of manually returning `impl Future`. |
| **API & Ergonomia** | [`m-avoid-wrappers`](rules/m-avoid-wrappers.md) | Microsoft Pragmatic Rust | Do not expose smart pointers (`Arc`, `Rc`, `Mutex`, `Box`) in public API signatures. |
| **API & Ergonomia** | [`m-di-hierarchy`](rules/m-di-hierarchy.md) | Microsoft Pragmatic Rust | Prefer concrete types over generics, and generics over `dyn Trait`. |
| **API & Ergonomia** | [`m-dont-leak-types`](rules/m-dont-leak-types.md) | Microsoft Pragmatic Rust | Do not expose internal foreign crate types in public API signatures without intentional re-exporting. |
| **API & Ergonomia** | [`m-init-builder`](rules/m-init-builder.md) | Microsoft Pragmatic Rust | Use the Builder pattern for structs with complex or optional configuration. |
| **API & Ergonomia** | [`m-regular-fn`](rules/m-regular-fn.md) | Microsoft Pragmatic Rust | Prefer regular standalone functions over empty dummy structs with associated functions. |
| **API & Ergonomia** | [`m-services-clone`](rules/m-services-clone.md) | Microsoft Pragmatic Rust | Make service and client handle structs cheaply `Clone` using internal shared state. |
| **API & Ergonomia** | [`m-weasel-words`](rules/m-weasel-words.md) | Microsoft Pragmatic Rust | Eliminate vague "weasel words" (Helper, Manager, Common, Data, Info) from names. |
| **Performance & Memória** | [`m-async-stack-size`](rules/m-async-stack-size.md) | Microsoft Pragmatic Rust | Box large state buffers across `.await` points to avoid giant future frame sizes. |
| **Performance & Memória** | [`m-box-dst`](rules/m-box-dst.md) | Microsoft Pragmatic Rust | Use `Box<[T]>` or `Box<str>` instead of `Vec<T>` or `String` for immutable owned sequences. |
| **Performance & Memória** | [`m-fast-hasher`](rules/m-fast-hasher.md) | Microsoft Pragmatic Rust | Use a fast non-cryptographic hasher (`ahash` or `foldhash`) for internal HashMaps. |
| **Performance & Memória** | [`m-shrink-to-fit`](rules/m-shrink-to-fit.md) | Microsoft Pragmatic Rust | Call `shrink_to_fit()` on long-lived collections after construction. |
| **Performance & Memória** | [`m-yield-points`](rules/m-yield-points.md) | Microsoft Pragmatic Rust | Insert cooperative yield points in long-running CPU-bound loops in async tasks. |
| **Performance & Memória** | [`mem-reuse-collections`](rules/mem-reuse-collections.md) | Pragmatic / Soundness | Clear and reuse existing buffer allocations across iterations instead of allocating new ones. |
| **Performance & Memória** | [`mem-with-capacity`](rules/mem-with-capacity.md) | Pragmatic / Soundness | Always call `with_capacity()` when the collection size is known or estimable. |
| **Apps, Resiliência & AI** | [`c-failure`](rules/c-failure.md) | Rust API Guidelines | Public API documentation must contain explicit `# Errors`, `# Panics`, and `# Safety` sections. |
| **Apps, Resiliência & AI** | [`m-app-error`](rules/m-app-error.md) | Microsoft Pragmatic Rust | Use `anyhow` for top-level application binary error handling, but never in library crates. |
| **Apps, Resiliência & AI** | [`m-cargo-workspace`](rules/m-cargo-workspace.md) | Microsoft Pragmatic Rust | Centralize all dependency versions under `[workspace.dependencies]` at the workspace root. |
| **Apps, Resiliência & AI** | [`m-design-for-ai`](rules/m-design-for-ai.md) | Microsoft Pragmatic Rust | Design APIs and modules for AI comprehension: idiomatic patterns, strong types, and testable examples. |
| **Apps, Resiliência & AI** | [`m-features-additive`](rules/m-features-additive.md) | Microsoft Pragmatic Rust | Cargo features must be strictly additive; enabling a feature must never disable functionality or break code. |
| **Apps, Resiliência & AI** | [`m-lint-override-expect`](rules/m-lint-override-expect.md) | Microsoft Pragmatic Rust | Use `#[expect(clippy::...)]` instead of `#[allow(clippy::...)]` for deliberate lint suppressions. |
| **Apps, Resiliência & AI** | [`m-log-not-print`](rules/m-log-not-print.md) | Microsoft Pragmatic Rust | Production code uses structured telemetry (`tracing`/`log`), never `println!`, `eprintln!`, or `dbg!`. |
| **Apps, Resiliência & AI** | [`m-log-structured`](rules/m-log-structured.md) | Microsoft Pragmatic Rust | Emit telemetry events and spans with explicit key-value fields rather than formatted string interpolation. |
| **Apps, Resiliência & AI** | [`m-mimalloc-apps`](rules/m-mimalloc-apps.md) | Microsoft Pragmatic Rust | Configure `mimalloc` as the global memory allocator in application binaries. |
| **Apps, Resiliência & AI** | [`m-mockable-syscalls`](rules/m-mockable-syscalls.md) | Microsoft Pragmatic Rust | Design core domain logic "sans I/O" or abstract system calls behind mockable traits. |
| **Apps, Resiliência & AI** | [`m-smaller-crates`](rules/m-smaller-crates.md) | Microsoft Pragmatic Rust | Decompose monolithic crates into smaller, single-responsibility workspace crates. |
| **Apps, Resiliência & AI** | [`m-test-util`](rules/m-test-util.md) | Microsoft Pragmatic Rust | Gate test fixtures, fakes, and harness utilities behind `feature = "test-util"`. |
| **Metaprogramação & Macros** | [`m-example-over-proc`](rules/m-example-over-proc.md) | Microsoft Pragmatic Rust | Prefer declarative `macro_rules!` (macros by example) over procedural macros when possible. |
| **Metaprogramação & Macros** | [`m-macro-helpers`](rules/m-macro-helpers.md) | Microsoft Pragmatic Rust | Re-export external third-party dependencies used in macro expansion under `#[doc(hidden)] pub mod _private`. |
| **Metaprogramação & Macros** | [`m-macro-last-resort`](rules/m-macro-last-resort.md) | Microsoft Pragmatic Rust | Treat macros as a tool of last resort; prefer functions, traits, and generics. |
| **Metaprogramação & Macros** | [`m-proc-impl`](rules/m-proc-impl.md) | Microsoft Pragmatic Rust | Separate procedural macro logic into an internal implementation crate with unit tests. |
| **Native FFI** | [`m-ffi-naming`](rules/m-ffi-naming.md) | Microsoft Pragmatic Rust | Exported C-ABI functions must follow the strict `<crate>_<type>_<method>` naming convention. |
| **Native FFI** | [`m-ffi-translates`](rules/m-ffi-translates.md) | Microsoft Pragmatic Rust | FFI crates must only translate types and calls; business logic belongs in pure Rust core crates. |
| **Native FFI** | [`m-isolate-dll-state`](rules/m-isolate-dll-state.md) | Microsoft Pragmatic Rust | Isolate global runtime state when exposing Rust libraries as dynamic libraries (DLLs/so/dylib). |

---

## 🚀 Como Instalar e Sincronizar (`sync.sh`)

O instalador universal agnóstico prepara o ambiente desejado em seu projeto:

### 1. Ambientes Suportados
```bash
./sync.sh antigravity /caminho/para/seu-projeto-rust   # Google Antigravity
./sync.sh opencode    /caminho/para/seu-projeto-rust   # OpenCode
./sync.sh kilocode    /caminho/para/seu-projeto-rust   # Kilo Code
./sync.sh cursor      /caminho/para/seu-projeto-rust   # Cursor (.cursor/rules/*.mdc)
./sync.sh claude      /caminho/para/seu-projeto-rust   # Claude Code (CLAUDE.md)
./sync.sh copilot     /caminho/para/seu-projeto-rust   # GitHub Copilot
./sync.sh all         /caminho/para/seu-projeto-rust   # Todos os ambientes
```

### 2. Comandos Utilitários (Zero Token Waste CLI)
```bash
# Busca regras por palavra-chave ou conceito
./sync.sh find memory

# Exibe o conteúdo completo de uma regra específica
./sync.sh query m-cargo-workspace

# Lista todas as regras disponíveis com seus imperativos
./sync.sh list

# Executa o suite de testes de integridade e verificação
./sync.sh verify

# Remove arquivos de diretrizes de forma limpa (ex: antigravity ou all)
./sync.sh clean antigravity /caminho/para/seu-projeto-rust
```

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para detalhes.
