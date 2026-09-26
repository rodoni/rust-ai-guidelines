# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato segue as convenções de [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/), e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.2.1] - 2026-09-25

### Corrigido (Fixed)
- **`m-errors-canonical`**: Reconciliada a diretriz com a fonte original Microsoft Pragmatic Rust (`M-ERRORS-CANONICAL-STRUCTS`), prescrevendo structs situacionais com `Backtrace` capturado e métodos de consulta (`is_syntax_error()`, `is_io()`), eliminando o vazamento de enums e tipos externos (`std::io::Error`).
- **`er-closure-traits`**: Removido disclaimer meta-textual do bloco imperativo e alinhada a explicação técnica da hierarquia de subtipagem de closures com a abordagem de traits fundamentais do *Effective Rust* (Item 10) e do ecossistema Rust.
- **`m-dont-leak-types`**: Eliminada ambiguidade entre encapsulamento de tipos estrangeiros e reexportação, correlacionando formalmente com [`er-reexport-dependencies`](rules/er-reexport-dependencies.md) para contratos públicos intencionais.
- **Atribuições de Origem no README**:
  - `m-ffi-naming`: Corrigida a atribuição de convenção local para **`Microsoft Pragmatic Rust (M-FFI-NAMING)`**.
  - `mem-reuse-collections`: Corrigida a atribuição de origem genérica para **`Microsoft Pragmatic Rust (M-MEM-REUSE)`**.
  - `mem-with-capacity`: Corrigida a atribuição de origem genérica para **`Microsoft Pragmatic Rust (M-INITIAL-CAPACITY)`**.
  - `m-unsound-prevention`: Vinculada explicitamente à regra **`Microsoft Pragmatic Rust (M-UNSOUND)`**.
  - `unsafe-safety-comment` e `unsafe-minimize-scope`: Atribuídas formalmente às convenções do Clippy (`clippy::undocumented_unsafe_blocks`) e Rustonomicon / Stdlib.
  - Inclusão do ecossistema *Rust Testing & Soundness Practices* no rol de fundamentos bibliográficos do [`README.md`](README.md).
- **Sincronização nos Agentes e Skills**: Atualizadas as descrições de erros canônicos em [`skills/rust-guidelines/SKILL.md`](skills/rust-guidelines/SKILL.md), [`skills/rust-safety/SKILL.md`](skills/rust-safety/SKILL.md) e [`agents/rust-safety-auditor.md`](agents/rust-safety-auditor.md).

---

## [1.2.0] - 2026-09-24

### Adicionado (Added)
- **Skill `rust-testing`**: Módulo dedicado a testes determinísticos, property-based testing, snapshots e fixtures mockáveis.
- **Agente `rust-test-engineer`**: Subagente especializado na elaboração e manutenção de suítes de testes determinísticos de alta cobertura e invariantes de domínio.
- **6 Regras Atômicas de Teste (`test-*`)**:
  - [`test-property-based`](rules/test-property-based.md): Testes baseados em propriedades com `proptest`.
  - [`test-assert-error-variants`](rules/test-assert-error-variants.md): Asserções estritas de variantes com `matches!` ou `assert_matches!`.
  - [`test-deterministic-no-sleep`](rules/test-deterministic-no-sleep.md): Eliminação de sleeps de relógio de parede em favor de tempo virtual (`tokio::time::pause()`).
  - [`test-fakes-over-heavy-mocks`](rules/test-fakes-over-heavy-mocks.md): Fakes leves em memória no lugar de frameworks de mocking com tempos de vida complexos.
  - [`test-behavior-not-internals`](rules/test-behavior-not-internals.md): Testes focados em comportamento observável e invariantes.
  - [`test-snapshot-for-complex-data`](rules/test-snapshot-for-complex-data.md): Testes de snapshot com `insta` para ASTs e estruturas complexas.
- Script de limpeza de artefatos temporários e distribuições [`scripts/clean-distributions.sh`](scripts/clean-distributions.sh).

### Modificado (Changed)
- Atualização do master hub [`skills/rust-guidelines/SKILL.md`](skills/rust-guidelines/SKILL.md) e matriz de mapeamento para versão 1.2.0.

---

## [1.1.0] - 2026-09-20

### Adicionado (Added)
- **Integração de 4 Novas Fontes Canônicas**:
  - *Rust Atomics and Locks* por Mara Bos: Regras atômicas e concorrência causal (`atomic-ordering-pair`, `atomic-cas-weak-loops`, `sync-avoid-spinlock`, `sync-cacheline-padding`, `sync-lock-hierarchy`).
  - *Effective Rust* por David Drysdale: Typestate, conversões seguras sem `as` numérico e RAII guards (`er-casts-avoid-as`, `er-typestate-pattern`, `er-raii-guard`, `er-reexport-dependencies`, `er-closure-traits`).
  - *Programming Rust* por Jim Blandy et al.: Layout de structs contra padding (`sys-struct-field-ordering`), iteradores zero-allocation (`sys-iterator-zero-allocation`) e tradeoffs de dispatch (`sys-dispatch-tradeoff`).
  - *Tweag Agentic Coding Handbook*: Workflows atômicos para agentes de IA (`wf-spec-first`, `wf-atomic-steps`, `wf-verification-gates`, `wf-tdd-loop`, `wf-debug-systematic`).
- **Critérios Estritos de Rejeição**: Enquadramento de Zero Tolerância nos agentes [`rust-safety-auditor`](agents/rust-safety-auditor.md) e [`rust-reviewer`](agents/rust-reviewer.md).

---

## [1.0.0] - 2026-09-15

### Adicionado (Added)
- **Lançamento Inicial**: Ecossistema de regras atômicas de baixíssimo consumo de contexto (*Zero Token Waste*).
- **Agentes Especializados**: `rust-lead`, `rust-api-architect`, `rust-perf-optimizer`, `rust-safety-auditor`, `rust-reviewer`.
- **Suíte de Skills Temáticas**: `rust-guidelines`, `rust-api`, `rust-perf`, `rust-concurrency`, `rust-safety`, `rust-macros`, `rust-ffi`, `rust-resilience-app`.
- **Regras Atômicas Iniciais**: Baseadas no *Official Rust API Guidelines* (C-*) e *Microsoft Pragmatic Rust Guidelines* (M-*).
- **Instalador Universal Multi-Ambiente (`sync.sh`)**: Suporte a Google Antigravity, OpenCode, Kilo Code, Cursor (`.mdc`), Claude Code e GitHub Copilot.
- **Suíte de Testes de Integridade (`scripts/verify.py`)**: Validação automatizada de estrutura de regras, links markdown e sincronização ponta a ponta.
