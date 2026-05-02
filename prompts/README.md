# Specialist prompts

Plain-text system prompts for use with any LLM runtime (cloud or local, e.g. `tooling/ollama-run.sh`).

| File | Role | When to use |
|------|------|-------------|
| `10th-man.txt` | Adversarial review, pre-mortem, kill criteria | Before committing to a risky architecture, rollout, or irreversible choice |
| `librarian.txt` | Distill messy notes/transcripts into tagged, durable summaries | After a session or task; before archiving or sharing widely |
| `broker.txt` | Cross-task overlap, dependency hypotheses, silo warnings | When starting work that might touch shared systems, teams, or prior decisions |
| `import-distill-onepager.txt` | **Paste-ready** distill of Slack/email exports → reasoning log + optional ADR; maps **participants** and **decision authority** tiers | Bootstrapping `.calyx/` from a file dump; pair with `templates/distill-external-to-calyx.md` for the long form |
| `distill-inbox-stub-onepager.txt` | Turn a **post-commit inbox stub** (`reasoning/inbox/auto-*.md`) into a reasoning log, ADR stub, or “delete noise” | After `install-calyx-git-hooks.sh`; see `docs/automation.md` |
| `promote-cpl-to-col.txt` | **Agent-assisted** lift from project **cpl** to org **col**: redact, propose org-repo file bodies + PR checklist; human merges | When `.calyx/org/` exists and a human authorizes sharing; see `.calyx/AGENT_ROLES.md` |
| `librarian-taxonomy-sync.txt` | Reconcile **`local-tags.yaml`** with **`master-tags.yaml`**; flag orphans; propose patches; optional **col** / **ccl** follow-ups | Pair with `templates/librarian-taxonomy-review.md` for a checklist |

Feed each prompt as the system or leading instruction block, then attach the **task-specific context** (and for Librarian, the taxonomy YAMLs). For **import distillation**, attach the export and any redaction rules. For **inbox stubs**, attach the stub file.

**Project index:** new repos get **`.calyx/AGENT_ROLES.md`** from **`tooling/calyx-install-agent-roles.sh`** (also run at end of **`calyx-setup-capture.sh`**). Brownfield: run the installer once; **`--force`** overwrites that file from core.
