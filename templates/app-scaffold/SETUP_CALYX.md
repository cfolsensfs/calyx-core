# Calyx setup — start here

**Project:** __PROJECT_NAME__

## If you are a human

1. Open this **repository root** in **Cursor** (whole tree, not a subfolder).
2. After **`git submodule update --init --recursive`**, read the full guide: **`.calyx/core/docs/first-run.md`** (prerequisites, **why** each exists, and the ordered checklist).
3. Run **`bash .calyx/core/tooling/calyx-setup-capture.sh`**, then **restart Cursor** (or reload hooks).
4. Run **`bash .calyx/core/tooling/calyx-verify-capture.sh`** — all lines should be **OK** (or follow **FAIL** hints). CI uses the same script with **`--ci`** (see **`.github/workflows/calyx-verify.yml`** if present).

## If you are a Cursor agent

The user (or lead dev) chose **Calyx**. Help them complete setup **from the repo root**:

1. Open and follow **`.calyx/core/docs/first-run.md`** step by step—**including verify commands** and the **restart Cursor** step after hooks are installed.
2. If **`.calyx/core`** is missing, do not improvise: use **`docs/new-project.md`** / **`docs/GIT.md`** in this repo to get the submodule in place first.
3. After **`calyx-setup-capture.sh`**, run **`calyx-verify-capture.sh`** with the user and resolve every **FAIL** before moving on.
4. After verify passes, suggest a **smoke test** (small commit + short chat) and point them to **`AGENTS.md`** for ongoing norms.

Reasoning for this two-layer flow: **one canonical doc** (`first-run.md`) avoids drift; **this file** is the obvious door in the repo and gives you clear instructions to read that doc.
