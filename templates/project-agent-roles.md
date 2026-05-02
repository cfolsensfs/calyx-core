# Calyx agent roles — this project

**cpl** helpers live in this file; **specialist prompts** live under **`.calyx/core/prompts/`** (submodule). Run prompts with your LLM front end (e.g. Cursor): paste the prompt file body as the system or leading instruction, then attach task-specific files.

## Capture → durable **cpl** (default loop)

| When | Prompt / artifact | Attach / context |
|------|-------------------|------------------|
| After a substantive commit | **`distill-inbox-stub-onepager.txt`** | `.calyx/reasoning/inbox/auto-*.md` |
| After a heavy session | **`librarian.txt`** | Chat excerpts, draft log, **`master-tags.yaml` + `local-tags.yaml`** |
| Slack / email dump | **`import-distill-onepager.txt`** + **`templates/distill-external-to-calyx.md`** | Export + redaction rules |

**Outputs** go under **`.calyx/reasoning/`**, **`.calyx/decisions/`**, and **`taxonomy/local-tags.yaml`** as appropriate.

## Taxonomy hygiene (cpl, then col / ccl if needed)

| When | Prompt / artifact | Attach |
|------|-------------------|--------|
| Tag drift, new themes, ADR vocabulary | **`librarian-taxonomy-sync.txt`** | `master-tags.yaml`, `local-tags.yaml`, optional org tags |
| Structured human checklist | **`templates/librarian-taxonomy-review.md`** (this bundle) | Same YAMLs |

## **cpl** → **col** (org layer) promotion

| When | Prompt | Preconditions |
|------|--------|----------------|
| Pattern is reusable, non-sensitive, studio-wide | **`promote-cpl-to-col.txt`** | **`.calyx/org/`** submodule (or col repo); human authorization; redaction |

You **propose** org-repo patches and a PR description; a **human** merges into **col**.

## Specialists (critique & visibility)

| Role | File |
|------|------|
| 10th Man | **`10th-man.txt`** |
| Broker | **`broker.txt`** |

## Refresh this file

Re-run **`bash .calyx/core/tooling/calyx-install-agent-roles.sh --force`** only if you want to reset this index from **calyx-core** (overwrites local edits to **this** file).

## Related

- **Root `AGENTS.md`** — layout rules and mandatory capture
- **`docs/workflow.md`** — rhythm diagram
- **`docs/glossary.md`** — **ccl** / **col** / **cpl**
