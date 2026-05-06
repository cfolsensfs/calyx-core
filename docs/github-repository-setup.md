# Hosting calyx-core on GitHub

Visibility, description, topics, releases, and traffic for this repository.

## Visibility

- **UI:** Repository **Settings** → **General** → **Danger Zone** → **Change repository visibility** → **Public**
- **CLI:** `gh auth login` then:
  ```bash
  gh repo edit cfolsensfs/calyx-core --visibility public --accept-visibility-change-consequences
  ```

## Description, topics, homepage

Short summary: [philosophy.md § In one sentence](philosophy.md#in-one-sentence). Example `gh repo edit` (after `gh auth login`):

```bash
gh repo edit cfolsensfs/calyx-core \
  --description "Calyx core — Git-native bundle for organizational reasoning: constitution, prompts, taxonomy, capture (Git+Cursor), weekly governance, change-to-evidence feedback loop, org lift & taxonomy prompts. Stewardship of thinking, not transcript mining." \
  --homepage "https://scalefreestrategy.com" \
  --add-topic knowledge-management --add-topic documentation --add-topic developer-tools \
  --add-topic ai --add-topic cursor --add-topic git --add-topic adr \
  --add-topic reasoning --add-topic organizational-learning
```

## License

Root **`LICENSE`**: **MIT**. If the UI does not pick it up after push: **Settings** → **General** → **License** → **MIT**.

## Release

**GitHub Release** from the current tag (e.g. **`v1.1.0`**); notes from [CHANGELOG.md](../CHANGELOG.md). New projects: pin **`v1.1.0`** or newer in `.calyx/core` ([new-project.md](new-project.md)).

## Traffic and stats

| Signal | Where | Notes |
|--------|--------|--------|
| **Clones** (unique cloners, traffic) | Repo **Insights** → **Traffic** | Visible to users with **maintainer/admin** access. Approximate; **not** a public “download counter.” |
| **Visitors** | **Insights** → **Traffic** | Page views on the GitHub UI; same access gate. |
| **Stars / forks** | Repo header | Public; rough interest proxy, not usage. |
| **Release assets** | Per-release download counts | Only if you attach **binaries**; **calyx-core** is source-only, so there are usually **no** release ZIP counts. |
| **`git` / submodule checkouts** | — | GitHub does **not** expose per-clone analytics for arbitrary `git clone` the way an app store does. Teams pin **tags**; you infer adoption from issues/PRs and your own telemetry if you add it. |

There is **no** built-in “Calyx downloads” metric. For a lightweight public signal, watch **Traffic** periodically or use the **GitHub API** (`/repos/{owner}/{repo}/traffic/clones`) with a token that has repo access—still **approximate** and **private** to the repo.

### Interest snapshot

Signals for **calyx-core** as a bundle (not stars alone):

1. **Stars + forks (+ open issues)** — public REST, no auth:
   ```bash
   curl -sS "https://api.github.com/repos/cfolsensfs/calyx-core" \
     | python3 -c "import sys,json; d=json.load(sys.stdin); print('stars', d['stargazers_count']); print('forks', d['forks_count']); print('open_issues', d['open_issues_count'])"
   ```
2. **Clone traffic** (~14 days, needs repo access) — e.g. GitHub CLI:
   ```bash
   gh api repos/cfolsensfs/calyx-core/traffic/clones
   ```
3. **Page-view traffic** (same window, same auth):
   ```bash
   gh api repos/cfolsensfs/calyx-core/traffic/views
   ```

Summarize **count / uniques** from the JSON plus **non-zero days** in `clones` and `views`. Note caveats: **approximate**, **CI/bots** may inflate clones, **unique** in daily buckets is not “unique people ever.”
