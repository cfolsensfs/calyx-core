# Releasing calyx-core

**Calyx v1** is the **first Git tag** consumers should pin for the capture baseline (`v1.0.0`). This file is for **maintainers** cutting that tag.

## Versioning (two numbers)

| What | Meaning |
|------|--------|
| **Git tag** (e.g. **`v1.0.0`**) | What project repos **checkout** in `.calyx/core` — “known-good release.” |
| **`manifest.yaml` → `version`** | Monotonic **bundle index** for sync/drift tooling. It does not have to match the Git tag digit-for-digit; it **must increase** when paths or semantics change. |

Document both in the GitHub **Release notes** when you publish.

## Pre-flight checklist (before `v1.0.0`)

1. **Scripts**
   ```bash
   cd /path/to/calyx-core
   for f in tooling/*.sh; do bash -n "$f" || exit 1; done
   ```
2. **Docs** — [first-run.md](first-run.md) renders cleanly; links to [automation.md](automation.md), [cursor-local-chat-log.md](cursor-local-chat-log.md), [constitution/CONSTITUTION.md](../constitution/CONSTITUTION.md) resolve.
3. **Smoke path** — from a **throwaway** scaffold or test repo: `git submodule update --init --recursive` → `calyx-setup-capture.sh` → restart Cursor → `calyx-verify-capture.sh` (no `FAIL`) → trivial commit → inbox or tune `CALYX_DIARY_MIN_LINES`; chat → `local/chat-log/` grows.
4. **CI template** — `templates/app-scaffold/github-workflows-calyx-verify.yml` references **`bash .calyx/core/tooling/calyx-verify-capture.sh --ci`** and **`submodules: recursive`**.
5. **Constitution** — [CONSTITUTION.md](../constitution/CONSTITUTION.md) still states **v1.0** and capture as load-bearing.
6. **License** — root **`LICENSE`** (MIT) is present; **README** links it.
7. **Public launch** — follow [github-repository-setup.md](github-repository-setup.md) for visibility, **About** text (or use copy in [philosophy.md](philosophy.md#for-github-repository-header)), topics, and GitHub Release from **`CHANGELOG.md`**.

## Tag and push

```bash
git checkout main   # or your release branch
git pull
# optional: bump manifest.yaml version and commit if the bundle index changed
git tag -a v1.0.0 -m "Calyx v1.0.0: first public release (capture baseline, philosophy, MIT license)"
git push origin main
git push origin v1.0.0
```

## After release

- **Consumer repos:** `cd .calyx/core && git fetch && git checkout v1.0.0` (or newer **v1.x.y**), then `calyx-setup-capture.sh` on each machine as needed.
- **Release notes:** mention **`calyx-setup-capture.sh`**, **`calyx-verify-capture.sh`**, **`SETUP_CALYX.md`**, **`docs/first-run.md`**, **`docs/philosophy.md`**, **`LICENSE`**, and optional **`.github/workflows/calyx-verify.yml`**.

## Related

- [new-project.md](new-project.md) — pinning submodules
- [README.md](../README.md) — consumer overview
