# Calyx UX flow

How someone goes from **“we want Calyx in our workspace”** to **steady habits** in the repo. For step-by-step commands, see [new-project.md](new-project.md).

## Incorporation flow

```mermaid
flowchart TB
  start([Want Calyx in this workspace])

  start --> fork{New project or existing repo?}

  fork -->|New| scaffold["Run tooling/scaffold-cursor-app.sh<br/>Optional: create-sfs-workspace.sh for folder + commit + GitHub"]
  fork -->|Existing| brown["Add git submodule → .calyx/core<br/>Create .calyx/reasoning, decisions, taxonomy<br/>Add or merge .cursorrules and AGENTS.md"]

  scaffold --> cursor[Open repository root in Cursor]
  brown --> cursor

  cursor --> sub["git submodule update --init --recursive"]

  sub --> daily[Day-to-day: ship work with people and AI]

  daily --> gate{Major or cross-cutting work?}

  gate -->|No| daily
  gate -->|Yes| log[Write reasoning log<br/>.calyx/reasoning/]

  log --> bind{Does a decision bind the future?}

  bind -->|No| daily
  bind -->|Yes| adr[Write or update ADR<br/>.calyx/decisions/]

  adr --> tags[Extend local-tags.yaml when vocabulary shifts]
  tags --> daily

  daily --> optional[Optional paths]
  optional --> org[Second submodule: .calyx/org<br/>studio-wide non-secret DNA]
  optional --> commons[Opt-in: promote sanitized patterns<br/>no raw transcripts]
```

## Reading the diagram

| Stage | What the user experiences |
|-------|---------------------------|
| **New vs existing** | Green field gets a one-command scaffold; brown field gets a short Git + folder merge—no rewrites. |
| **Cursor** | Workspace root = whole repo so `.cursorrules` applies everywhere. |
| **Submodule** | `.calyx/core` is the pinned calyx-core bundle; init once per clone. |
| **Major work gate** | Not every edit gets a log—only work where “why” should survive. |
| **ADR** | For choices that constrain tomorrow’s work; supersede, don’t silently rewrite. |
| **Optional** | Org layer for agency defaults; “commons” only when explicitly sanitized and shared. |

## Related

- [new-project.md](new-project.md) — scripts, flags, deliverables
- [workflow.md](workflow.md) — ongoing Calyx **work** rhythm (reasoning, ADRs, checkpoint)
- [glossary.md](glossary.md) — **ccl** / **col** / **cpl**
- [README](../README.md) — repo overview and quick commands
