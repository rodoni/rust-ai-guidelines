# Rust AI Guidelines & Agentic Tools

Conjunto modular de **Agentes de IA** e **SKILLS** otimizados para desenvolvimento agêntico em Rust com **foco em baixíssimo consumo de contexto** (*Zero Token Waste*). 

Este ecossistema combina integralmente as diretrizes oficiais:
- [Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)
- [Official Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

Inspirado na arquitetura e concisão do repositório [`leonardomso/rust-skills`](https://github.com/leonardomso/rust-skills), o projeto divide o conhecimento em regras atômicas, eliminando documentações gigantescas que sobrecarregam a janela de contexto das LLMs e causam alucinações.

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
| **`rust-api-architect`** | [`rust-api`](skills/rust-api/SKILL.md) *(API & Ergonomia)* | `rust-resilience-app`, `rust-macros` | `c-case`, `c-conv`, `c-getter`, `c-common-traits`, `c-send-sync`, `c-newtype`, `c-sealed`, `m-weasel-words`, `m-regular-fn`, `m-avoid-wrappers`, `m-di-hierarchy`, `m-init-builder`, `m-services-clone`, `m-async-fn`, `m-macro-last-resort`, `m-example-over-proc`, `m-proc-impl`, `m-macro-helpers` |
| **`rust-perf-optimizer`** | [`rust-perf`](skills/rust-perf/SKILL.md) *(Memória & Async)* | `rust-api`, `rust-resilience-app` | `mem-with-capacity`, `mem-reuse-collections`, `m-box-dst`, `m-shrink-to-fit`, `m-fast-hasher`, `m-async-stack-size`, `m-yield-points`, `m-mimalloc-apps` |
| **`rust-safety-auditor`** | [`rust-safety`](skills/rust-safety/SKILL.md) *(Soundness & Erros)* | [`rust-ffi`](skills/rust-ffi/SKILL.md), `rust-api` | `unsafe-safety-comment`, `unsafe-minimize-scope`, `m-unsound-prevention`, `m-panic-on-bug`, `m-errors-canonical`, `m-ffi-translates`, `m-isolate-dll-state` |
| **`rust-reviewer`** | [`rust-resilience-app`](skills/rust-resilience-app/SKILL.md) *(Lints & Contratos)* | `rust-safety`, `rust-api`, `rust-perf` | `m-lint-override-expect`, `c-failure`, `m-macro-helpers`, `m-test-util`, `m-app-error`, `m-design-for-ai` |


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
