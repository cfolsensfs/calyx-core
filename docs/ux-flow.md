# Calyx UX flow

How someone goes from **“we want Calyx in our workspace”** to **steady habits** in the repo. For step-by-step commands, see [new-project.md](new-project.md).

## Incorporation flow

```mermaid
flowchart TB
  start([Want Calyx in this workspace])

  start --> fork{New project or existing repo?}

  fork -->|New| scaffold["Run tooling/scaffold-cursor-app.sh<br/>→ .cursor/hooks + hooks.json<br/>→ turns append to local/chat-log/"]
  fork -->|Existing| brown["Add git submodule → .calyx/core<br/>Create .calyx/reasoning, decisions, taxonomy<br/>Add or merge .cursorrules and AGENTS.md<br/>v1: bash .calyx/core/tooling/calyx-setup-capture.sh"]

  scaffold --> cursor[Open repository root in Cursor]
  brown --> cursor

  cursor --> chatTrail["Session trail: hook events → local/chat-log/<br/>gitignored; default retention ~3 days"]
  chatTrail --> sub["git submodule update --init --recursive"]

  sub --> daily[Day-to-day: ship work with people and AI]

  daily --> gate{Major or cross-cutting work?}

  gate -->|No| daily
  gate -->|Yes| log[Write reasoning log<br/>.calyx/reasoning/]

  log --> bind{Does a decision bind the future?}

  bind -->|No| daily
  bind -->|Yes| adr[Write or update ADR<br/>.calyx/decisions/]

  adr --> tags[Extend local-tags.yaml when vocabulary shifts]
  tags --> daily

  daily --> optionalStudio[Optional studio paths]
  optionalStudio --> org[Second submodule: .calyx/org<br/>studio-wide non-secret DNA]
  optionalStudio --> commons[Opt-in: promote sanitized patterns<br/>no raw transcripts]

  daily -.-> eod["Regular distill:<br/>local/chat-log + inbox stubs + diff<br/>→ reasoning or delete noise"]
  eod -.-> daily
```

## Reading the diagram

| Stage | What the user experiences |
|-------|---------------------------|
| **New vs existing** | Green field gets a one-command scaffold; brown field gets a short Git + folder merge—no rewrites. |
| **Cursor** | Workspace root = whole repo so `.cursorrules` applies everywhere. |
| **Session trail** | **Calyx v1** expects **Cursor hooks** so each turn appends under **`local/chat-log/`**—raw material for distill. Install with **`calyx-setup-capture.sh`** or scaffold. See [cursor-local-chat-log.md](cursor-local-chat-log.md). |
| **Submodule** | `.calyx/core` is the pinned calyx-core bundle; init once per clone. |
| **Distill rhythm** | Use recent **`local/chat-log/*.md`** with **inbox stubs** ([automation.md](automation.md)) and **git diff** so “why” in chat can land in **`.calyx/reasoning/`** without retyping. For **cpl → col** and taxonomy, follow **`.calyx/AGENT_ROLES.md`** after **`calyx-install-agent-roles.sh`**. |
| **Major work gate** | Not every edit gets a log—only work where “why” should survive. |
| **ADR** | For choices that constrain tomorrow’s work; supersede, don’t silently rewrite. |
| **Optional studio** | Org layer for agency defaults; “commons” only when explicitly sanitized and shared. |

## Automation in the loop (quick reference)

| Mechanism | Output | Doc |
|-----------|--------|-----|
| **`calyx-setup-capture.sh`** | Installs git + Cursor capture (v1 baseline) | [automation.md](automation.md) |
| **Cursor hooks** + script | `local/chat-log/YYYY-MM-DD.md` (rolling retention) | [cursor-local-chat-log.md](cursor-local-chat-log.md) |
| **Post-commit hook** | `.calyx/reasoning/inbox/*.md` stubs | [automation.md](automation.md) |
| **Human / Librarian distill** | `.calyx/reasoning/` entries, ADRs when ratified | [workflow.md](workflow.md) |

## Related

- [first-run.md](first-run.md) — prerequisites, **why**, checklist; agent playbook for onboarding
- [new-project.md](new-project.md) — scripts, flags, deliverables
- [cursor-local-chat-log.md](cursor-local-chat-log.md) — install, limits, retention env var
- [automation.md](automation.md) — post-commit inbox stubs
- [workflow.md](workflow.md) — ongoing Calyx **work** rhythm (reasoning, ADRs, checkpoint)
- [glossary.md](glossary.md) — **ccl** / **col** / **cpl**
- [README](../README.md) — repo overview and quick commands
