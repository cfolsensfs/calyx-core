# Calyx glossary

Short names for the three **Calyx layers** in a project repo. Use full names in public docs for clarity; **abbreviations** are handy in internal notes, commit trailers, diagrams, and chat.

| Abbrev. | Layer | Meaning | Typical location |
|---------|--------|---------|------------------|
| **ccl** | **Calyx core layer** | Generic, forkable bundle: constitution, specialist prompts, master taxonomy, canonical templates, tooling. | Git submodule **`.calyx/core/`** → [calyx-core](https://github.com/cfolsensfs/calyx-core) repo. |
| **col** | **Calyx org layer** | Organization- or studio-wide defaults: non-sensitive playbooks, shared norms, local tag extensions for the org. | Optional Git submodule **`.calyx/org/`** (e.g. agency repo). |
| **cpl** | **Calyx project layer** | Engagement-specific reasoning, ADRs, and project taxonomy—what belongs to **this** repo only. | **`.calyx/reasoning/`**, **`.calyx/decisions/`**, **`.calyx/taxonomy/local-tags.yaml`** (not a separate submodule). |

**Precedence (typical):** **cpl** overrides **col** overrides **ccl** for a given topic—unless an ADR says otherwise.

**This repository** (`calyx-core`) **is** the source for **ccl** when mounted as `.calyx/core/`.

---

## Related

- [README](../README.md) — consumption model
- [new-project.md](new-project.md) — scaffolding
- [workflow.md](workflow.md) — ongoing rhythm
