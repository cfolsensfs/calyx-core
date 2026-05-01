# Runbook: distill external threads into Calyx artifacts

Use this when someone provides an **export or paste** from Slack, email, Teams, etc., and wants **project- or org-level Calyx** material—not a transcript dump in Git.

**Paste-ready shortcut:** [`prompts/import-distill-onepager.txt`](../prompts/import-distill-onepager.txt) — same job in one block; use for Cursor/CLI when you do not need this long checklist.

**Your job:** separate **chaff** from **wheat**, then emit **structured** outputs a human can review and commit.

---

## Inputs (ask if missing)

1. **Raw source** — file(s), paste, or path references the user will attach.
2. **Scope** — *project* (this engagement) vs *org* (studio-wide patterns). Affects tone and what belongs in `local-tags.yaml` vs future org layer.
3. **Redaction rules** — e.g. strip client legal names, personal emails, phone numbers; or “internal only, names OK.” Default: **minimize PII** in outputs; refer to roles (“PM”, “lead engineer”) unless user says otherwise.
4. **Target repo layout** — confirm they use `.calyx/reasoning/` and `.calyx/decisions/` (or org equivalent).

---

## Principles

- **Do not** reproduce full threads in the final artifacts unless the user explicitly wants an appendix and policy allows it.
- **Prefer** summarized claims with **source pointers** (“Slack #delivery, ~2026-04-12 thread about API auth”) over verbatim quotes.
- **Label uncertainty:** if the dump is ambiguous, say what is **inferred** vs **explicit** in the thread.
- **Noise is normal:** stand-ups, scheduling, emoji-only, and side jokes—**discard** unless they encode a decision.

---

## Step 1 — Classify segments

Scan the dump and tag each *coherent chunk* as one or more of:

| Tag | Meaning |
|-----|---------|
| `noise` | No durable reasoning (logistics, banter, duplicates). |
| `context` | Background only—useful for a reasoning log, not an ADR alone. |
| `option` | A named approach someone proposed. |
| `concern` | Risk, constraint, or objection. |
| `decision` | “We will / we won’t / we chose X”—explicit or strongly implied. |
| `open` | Unresolved question at end of thread. |

---

## Step 2 — Participants, roles, and authority (onboarding jumpstart)

Before summarizing the argument, map **who** was in the thread and how their input relates to **project outcomes**:

1. **Participant ledger** — for each person/handle: what they contributed (claims, options, objections, questions).
2. **Roles** — use labels from the source when explicit; otherwise `unknown_role` until a human confirms.
3. **Authority tier (for this project)** — not “who is smarter,” but **who can bind or own delivery** for this engagement:
   - **BINDING** — approval / veto / budget / formal sign-off.
   - **ACCOUNTABLE** — DRI or owner for a delivery slice (e.g. tech lead for architecture, PM for scope doc).
   - **CONSULTED** — specialty gate (security, legal, data) when invoked.
   - **CONTRIBUTOR** — substantive input without sole accountability.
   - **OBSERVER** — lightweight or informational participation.

Mark each tier **stated** vs **inferred**. If two **BINDING** voices disagree and the thread does not resolve it, capture that as an **open question**—do not force one ADR.

## Step 3 — Extract wheat

For everything **not** `noise`, produce a **bullet list** (working notes, not final prose):

- **Claims** — what was asserted (one line each).
- **Options considered** — name + who favored / who pushed back (use roles/handles per redaction rules).
- **Decisions** — only if clearly stated or clearly ratified; mark **inferred** if needed.
- **Open questions** — what a human must still confirm.

If there are **no** decisions or substantive tradeoffs, **stop** after a short reasoning log titled “Context import” and do **not** invent an ADR.

---

## Step 4 — Emit artifacts

### A. Reasoning log draft (required if there is any wheat)

Use the shape of `.calyx/reasoning/_TEMPLATE.md` (or `core/templates/reasoning-log.md` once the submodule exists). Include:

- **Title** — e.g. `Import: <topic> (from Slack/email)`.
- **Context** — what problem the thread was about.
- **Source** — channel/tool + approximate date range; no full paste.
- **Participants & authority** — table from Step 2 (ledger + tiers).
- **Thought stream** — chronological **summary** of how the discussion moved (not transcript).
- **Options considered** — table if helpful.
- **Outcome** — what was decided or that nothing was decided.
- **Artifacts** — “ADR stub below” or “none; context only.”
- **Open items** — explicit list.

### B. ADR stub (only if a **binding** or clearly ratified decision exists)

Use `.calyx/decisions/ADR-TEMPLATE.md`. Status **`proposed`** until a human ratifies.

- **Context** — 3–6 sentences.
- **Decision** — one clear statement.
- **Consequences** — positives, risks, follow-ups.
- If the thread **conflicts** with itself, **do not** force a single ADR—split into **open questions** in the reasoning log instead.

### C. Tag suggestions (optional)

If recurring themes appear, suggest **new `project_tags`** entries for `local-tags.yaml` (ids + one-line descriptions)—do not redefine core tag meanings.

---

## Step 5 — Handoff checklist

Tell the human:

1. **Review** redaction and inferred decisions—imports are **error-prone**.
2. **Edit** titles and filenames to match repo conventions (`YYYY-MM-DD-…` if they use dates).
3. **`git add` + commit** `.calyx/` with a message like `calyx: distill import — <topic>`.
4. **Ratify** ADR status when the team agrees.

---

## What not to do

- Don’t turn the repo into a **forensic archive** of every message.
- Don’t **invent** decisions to “clean up” messy threads.
- Don’t move **secrets** or credentials from dumps into Calyx—redact and point to a secret manager.

---

## Related

- One-pager prompt: `prompts/import-distill-onepager.txt`
- Reasoning template: `reasoning-log.md`
- ADR template: `adr.md`
- Ongoing rhythm: `docs/workflow.md` (in calyx-core repo root)
