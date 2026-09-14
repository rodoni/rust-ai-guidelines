# Rust AI Guidelines & Agentic Tools

Conjunto modular de **Agentes de IA** e **SKILLS** otimizados para desenvolvimento agêntico em Rust com **foco em baixíssimo consumo de contexto** (*Zero Token Waste*). 

Este ecossistema combina integralmente as diretrizes oficiais:
- [Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)
- [Official Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

Inspirado na arquitetura e concisão do repositório [`leonardomso/rust-skills`](https://github.com/leonardomso/rust-skills), o projeto divide o conhecimento em regras atômicas, eliminando documentações gigantescas que sobrecarregam a janela de contexto das LLMs e causam alucinações.

---

## 🎯 Compatibilidade Multi-Ambiente

Projetado para funcionar de forma nativa e sem fricção em múltiplos ambientes:
- **Google Antigravity** (`.agents/skills/` e `AGENTS.md`)
- **OpenCode / OpenCodeInterpreter** (`.opencode/` e `AGENTS.md`)
- **Kilo Code / Cursor / Windsurf** (`.kilocode/` e custom instructions)

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
- **When Acceptable**: Casos válidos de exceção.

---

## 🚀 Como Instalar e Sincronizar (`sync.sh`)

O repositório inclui um instalador universal agnóstico que prepara o ambiente desejado em seu projeto:

### 1. Antigravity
Configura `.agents/skills/`, `.agents/rules/` e o arquivo `AGENTS.md`:
```bash
./sync.sh antigravity /caminho/para/seu-projeto-rust
```

### 2. OpenCode
Configura `.opencode/rules/` e `AGENTS.md`:
```bash
./sync.sh opencode /caminho/para/seu-projeto-rust
```

### 3. Kilo Code / Cursor
Configura `.kilocode/rules/` e as instruções customizadas:
```bash
./sync.sh kilocode /caminho/para/seu-projeto-rust
```

### 4. Todos os Ambientes
```bash
./sync.sh all /caminho/para/seu-projeto-rust
```

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para detalhes.
