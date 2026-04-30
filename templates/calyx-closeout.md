# Calyx checkpoint (EOD brain sync)

**Name:** **Calyx checkpoint** — end-of-day ritual to push the **project brain** (and optional submodule pins) so work does not stay only on your machine.

Do this when you touched reasoning, ADRs, local tags, or bumped `.calyx/core` / `.calyx/org`.

## Quick checklist

1. **Review** — Open `git status`. Ensure no secrets in `.calyx/reasoning/` or commits.
2. **Finish stubs** — Move or delete `reasoning/inbox/*` session stubs after distilling (if you use hooks).
3. **Submodule pins** (only if you intentionally updated core/org today):
   ```bash
   cd .calyx/core && git fetch origin && git checkout main && git pull && cd ../..
   cd .calyx/org && git fetch origin && git checkout main && git pull && cd ../..
   git add .calyx/core .calyx/org
   ```
4. **Commit project brain + Calyx config**
   ```bash
   git add .calyx/ .cursorrules
   ```
   Add application code too if it belongs in the same checkpoint:
   ```bash
   git add -A
   ```
5. **Commit**
   ```bash
   git commit -m "calyx: checkpoint — <short topic, e.g. EstateAIgent scoring notes>"
   ```
6. **Push**
   ```bash
   git push
   ```

## Optional: helper script

From the **project repo root** (not inside `calyx-core`):

```bash
./.calyx/core/tooling/calyx-closeout.sh
```

It stages `.calyx/` and `.cursorrules` and shows status — you still write the commit message and push.

## If you only changed `calyx-core` or org repos

Those changes are **separate commits** in `calyx-core` / `calyx-scalefree-org`, then **bump** the submodule pointer in each consumer project (step 3–6 above).
