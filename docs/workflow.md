# Calyx workflow

**Living document.** This page describes the **ongoing work rhythm** after onboarding (contrast: [ux-flow.md](ux-flow.md)). When Calyx habits, templates, or tooling change materially, **update this file** and note it in `manifest.yaml` / release notes so downstream repos know to refresh expectations.

---

## Work rhythm (diagram)

```mermaid
flowchart TB
  begin([Start: task, spike, or session])

  begin --> work[Work with code, docs, and AI<br/>in the project repo]

  work --> major{Major or cross-cutting?<br/>architecture, security, data, infra, multi-person impact}

  major -->|No| work
  major -->|Yes| draft[Capture thinking in .calyx/reasoning/<br/>use _TEMPLATE or core/templates/reasoning-log.md]

  draft --> specialists{Need structured critique<br/>or distillation?}

  specialists -->|10th Man| t10[Run adversarial review<br/>.calyx/core/prompts/10th-man.txt]
  specialists -->|Librarian| lib[Distill + tag<br/>.calyx/core/prompts/librarian.txt]
  specialists -->|Broker| bro[Map dependencies / silos<br/>.calyx/core/prompts/broker.txt]
  specialists -->|Skip| bind

  t10 --> bind
  lib --> bind
  bro --> bind

  bind{Decision binds future work?}

  bind -->|No| tags
  bind -->|Yes| adr[ADR in .calyx/decisions/<br/>proposed → ratified → superseded]

  adr --> tags[Update .calyx/taxonomy/local-tags.yaml<br/>when project vocabulary shifts]

  tags --> link[Link: PRs / tickets ↔ reasoning + ADR]

  link --> checkpoint{Calyx artifacts<br/>changed today?}

  checkpoint -->|No| work
  checkpoint -->|Yes| sync[Calyx checkpoint:<br/>review, commit, push .calyx + .cursorrules]

  sync --> work
```

**Checkpoint detail:** see **`templates/calyx-closeout.md`** in this repo (mounted as **`.calyx/core/templates/calyx-closeout.md`** in projects) and **`tooling/calyx-closeout.sh`**.

---

## Stage guide

| Stage | Intent | Typical artifacts |
|-------|--------|-------------------|
| **Work** | Ship value; use AI like a teammate, not a black box. | Code, tests, product docs. |
| **Major gate** | Avoid logging noise; **do** log when “why” should survive the week. | — |
| **Reasoning log** | Chronological + options + outcome; dead ends are valuable. | `.calyx/reasoning/*.md` |
| **Specialists** | Optional prompts for challenge, summary, cross-team visibility. | Paste or run against session notes. |
| **ADR** | Ratify what future-you must not re-litigate silently. | `.calyx/decisions/ADR-*.md` |
| **Tags** | Keep local vocabulary aligned with `master-tags.yaml`. | `local-tags.yaml` |
| **Link** | Make the brain navigable from delivery work. | PR description, footnotes in tickets. |
| **Checkpoint** | Brain is not “local only” by accident. | `git commit` / `git push` |

---

## ADR lifecycle (compact)

```mermaid
stateDiagram-v2
  [*] --> proposed: Draft ADR
  proposed --> ratified: Team agrees this binds work
  ratified --> superseded: New ADR obsoletes old choice
  proposed --> abandoned: Idea rejected before adoption
  superseded --> [*]
  abandoned --> [*]
  ratified --> ratified: Minor clarifications only<br/>(prefer supersede for reversals)
```

When **superseding**, keep the old ADR file and record **Supersedes** / **Superseded by** links—do not rewrite history for tidiness.

---

## Commit-triggered inbox stubs (opt-in)

Install **`tooling/install-calyx-git-hooks.sh`** so **post-commit** writes **`.calyx/reasoning/inbox/auto-*.md`** for substantive commits; distill with **`prompts/distill-inbox-stub-onepager.txt`**. Full detail: [automation.md](automation.md).

## Bootstrapping from Slack / email exports

Raw exports are **mostly chaff**. Use an agent (or a human) to **classify, summarize, and structure**—not to archive full threads in Git.

**Runbook (for agents):** [`templates/distill-external-to-calyx.md`](../templates/distill-external-to-calyx.md) — produces a **reasoning log draft** and an **ADR stub** only when a binding decision exists; includes participant **authority tiers** (BINDING / ACCOUNTABLE / …), redaction, and handoff steps.

**One-pager (paste-ready):** [`prompts/import-distill-onepager.txt`](../prompts/import-distill-onepager.txt) — same intent in a single block for Cursor or other LLM front ends.

---

## Related

| Doc | Focus |
|-----|--------|
| [ux-flow.md](ux-flow.md) | First-time incorporation (scaffold vs brownfield, Cursor, submodule). |
| [new-project.md](new-project.md) | Scripts, flags, deliverables for new repos. |
| [README](../README.md) | Repo overview and quick commands. |
| [distill-external-to-calyx.md](../templates/distill-external-to-calyx.md) | Import / distillation runbook for noisy exports |
| [import-distill-onepager.txt](../prompts/import-distill-onepager.txt) | Paste-ready import distillation prompt |
| [glossary.md](glossary.md) | **ccl** / **col** / **cpl** layer abbreviations |
| [org-and-projects.md](org-and-projects.md) | Agency/org vs project repos |
| [automation.md](automation.md) | Post-commit inbox stubs, skip flags, distill |
| [cursor-local-chat-log.md](cursor-local-chat-log.md) | Cursor hooks → `local/chat-log/` for optional EOD distill |
