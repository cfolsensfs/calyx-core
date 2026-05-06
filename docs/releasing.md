# Releasing calyx-core

**Current recommended pin for new consumers:** **`v1.1.0`** (see [CHANGELOG.md](../CHANGELOG.md)). **`v1.0.0`** remains the first public capture baseline. This file is for **maintainers** cutting tags.

## Versioning (two numbers)

| What | Meaning |
|------|--------|
| **Git tag** (e.g. **`v1.1.0`**) | What project repos **checkout** in `.calyx/core` — “known-good release.” |
| **`manifest.yaml` → `version`** | Monotonic **bundle index** for sync/drift tooling. It does not have to match the Git tag digit-for-digit; it **must increase** when paths or semantics change. |

Document both in the GitHub **Release notes** when you publish.

## Pre-flight checklist (before any new `v1.x.y` tag)

1. **Scripts**
   ```bash
   cd /path/to/calyx-core
   for f in tooling/*.sh; do bash -n "$f" || exit 1; done
   ```
   ```bash
   python3 -m unittest discover -s tooling/tests -p "test_*.py"
   ```
2. **Docs** — [first-run.md](first-run.md) renders cleanly; links to [automation.md](automation.md), [cursor-local-chat-log.md](cursor-local-chat-log.md), [constitution/CONSTITUTION.md](../constitution/CONSTITUTION.md) resolve.
3. **Smoke path** — from a **throwaway** scaffold or test repo: `git submodule update --init --recursive` → `calyx-setup-capture.sh` → restart Cursor → `calyx-verify-capture.sh` (no `FAIL`) → trivial commit → inbox or tune `CALYX_DIARY_MIN_LINES`; chat → `local/chat-log/` grows.
4. **CI template** — `templates/app-scaffold/github-workflows-calyx-verify.yml` references **`bash .calyx/core/tooling/calyx-verify-capture.sh --ci`** and **`submodules: recursive`**.
5. **Constitution** — [CONSTITUTION.md](../constitution/CONSTITUTION.md) still states **v1.0** and capture as load-bearing.
6. **License** — root **`LICENSE`** (MIT) is present; **README** links it.
7. **CHANGELOG** — new tag section with user-facing summary.
8. **Consumer docs** — [README.md](../README.md), [new-project.md](new-project.md), and related pins mention the **new** tag when it becomes the recommended default.

## Tag and push

Replace **`v1.1.0`** / message with the new version:

```bash
git checkout main   # or your release branch
git pull
# commit: changelog + manifest bump if bundle index changed
git tag -a v1.1.0 -m "Calyx v1.1.0: agent roles, cpl→col + taxonomy prompts (recommended pin)"
git push origin main
git push origin v1.1.0
```

## After release

- **Consumer repos:** `cd .calyx/core && git fetch && git checkout v1.1.0` (or newer **v1.x.y**), then `calyx-setup-capture.sh` on each machine as needed.
- **GitHub:** create a **Release** from the tag; paste from [CHANGELOG.md](../CHANGELOG.md).
- **Release notes:** mention **`calyx-setup-capture.sh`**, **`calyx-verify-capture.sh`**, **`calyx-install-agent-roles.sh`**, **`calyx-eow-governance.sh`**, **`calyx-feedback-loop.sh`**, **`SETUP_CALYX.md`**, **`docs/first-run.md`**, **`docs/eow-governance.md`**, **`docs/feedback-loop.md`**, **`docs/philosophy.md`**, **`LICENSE`**, and optional **`.github/workflows/calyx-verify.yml`** / **`calyx-feedback.yml`**.

## Related

- [new-project.md](new-project.md) — pinning submodules
- [README.md](../README.md) — consumer overview
- [github-repository-setup.md](github-repository-setup.md) — visibility, **Traffic** / stats expectations
