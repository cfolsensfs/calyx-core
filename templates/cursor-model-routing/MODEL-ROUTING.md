# Model routing (Cursor)

**Purpose:** Pick the model that fits the **task**, not the default that is fastest. Copy this file to **`agents/MODEL-ROUTING.md`** in your project (or keep it under `docs/` if you prefer). Pair with **`.cursor/rules/model-routing.mdc`** (`alwaysApply: true`) from the same Calyx template bundle.

**Useful with or without Calyx:** routing is operator discipline in Cursor; Calyx only ships and versions the kit.

---

## Before you act (every thread)

1. Classify the request: `task_type`, `deliverable`, `stakes` (internal vs client-visible vs legal-adjacent).
2. Choose a model from the table below (state in one line if the user did not specify: `Model: … because …`).
3. Escalate once if the first attempt fails or stakes are high; do not burn the hardest model on typos or the fastest model on binding copy.

When you **distill** into Calyx reasoning logs or ADRs, preserve **model** and **escalation** if stated in the thread (see optional **Agent context** in templates).

---

## Capability tiers (remap when Cursor renames products)

| Tier | Typical use |
|------|-------------|
| **fast implementation** | Clear-scope repo edits, scripts, git, small fixes |
| **balanced** | Mixed code + docs, internal planning, Calyx reasoning drafts |
| **deep code** | App stack, tooling, refactors, debug after one failed fix |
| **client prose** | External copy, long docs, doc MCP, style guides |
| **hard judgment** | Scope ambiguity, strategy, stuck twice, high-stakes compliance |

---

## Available models (example stack — edit for your team)

| Model | Tier | Use when |
| ----- | ---- | -------- |
| **Composer 2** | fast implementation | Clear-scope implementation, repo edits, scripts, git |
| **GPT-5.5** | balanced | Mixed code + docs, research, internal planning |
| **GPT-5.3 Codex** | deep code | App code, tooling, refactors, debugging |
| **Sonnet 4.6** | client prose | Client-facing writing, long docs, MCP doc edits |
| **Opus 4.7** | hard judgment | Ambiguous scope, strategy, stuck after two tries |

**Anti-patterns**

- Fast implementation tier for client-facing or legal-adjacent claims without a prose-tier pass.
- Hard-judgment tier for single-line fixes or formatting nits.
- Cloud models for bulk PII when offline redaction should run first (see Ollama below).

---

## Routing table (by task type)

| Task type | Primary model | Escalate to |
| --------- | ------------- | ----------- |
| Code / app / scripts / CI | Composer 2 | Codex 5.3 |
| Infra / build failures | Codex 5.3 | Opus 4.7 |
| Client-facing copy | Sonnet 4.6 | Opus 4.7 |
| External doc MCP (Google Docs, etc.) | Sonnet 4.6 | Opus 4.7 |
| Analytics / metrics narrative | Sonnet 4.6 | Opus 4.7 |
| PM / contract / scope | GPT-5.5 | Opus 4.7 |
| Research (internal) | GPT-5.5 | Sonnet 4.6 if client-ready |
| Calyx reasoning / ADR draft | GPT-5.5 | Opus 4.7 for durable architecture decisions |
| Quick one-file fix | Composer 2 | (rarely) |

Pair with specialist prompts when relevant (10th Man, Librarian, Broker under `.calyx/core/prompts/`).

---

## Project-specific (edit per repo — **cpl**)

<!-- Example:
- **Client / engagement:** …
- **Client prose guide:** `agents/CLIENT-FACING-PROSE.md`
- **Legal path:** `local/legal/…`
- **Doc registry:** `docs/…`
- **Specialist agents:** `agents/<role>/IDENTITY.md`
-->

_(Add project name, client prose path, legal path, doc registry, and specialist agent pointers here.)_

---

## Ollama (optional)

Local models via **`bash .calyx/core/tooling/ollama-run.sh`** (when Calyx is installed): offline drafts and redaction only — **not** primary for MCP / multi-tool agent sessions in Cursor.

---

## Install checklist

1. `agents/MODEL-ROUTING.md` ← this file (with **Project-specific** filled in)
2. `.cursor/rules/model-routing.mdc` ← from `templates/cursor-model-routing/model-routing.mdc` in calyx-core
3. `AGENTS.md`: session start includes model routing (scaffold adds this by default)
4. Enable the same models in **Cursor Settings** for the team
