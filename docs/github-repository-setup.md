# GitHub repository setup (visibility, About, releases)

Use this when publishing or refreshing **calyx-core** on GitHub. **Description and topics** can be set in the GitHub UI (**Settings** or the gear on the repo **About** sidebar) or with **`gh`** (see below).

## Visibility

- **UI:** Repository **Settings** → **General** → **Danger Zone** → **Change repository visibility** → **Public** (read the warnings).
- **CLI:** `gh auth login` then:
  ```bash
  gh repo edit cfolsensfs/calyx-core --visibility public --accept-visibility-change-consequences
  ```

## About (description + topics + homepage)

The canonical copy lives under **[philosophy.md — For GitHub](philosophy.md#for-github-repository-header)**.

**CLI example** (after `gh auth login`):

```bash
gh repo edit cfolsensfs/calyx-core \
  --description "Calyx core — Git-native bundle for organizational reasoning: constitution, prompts, taxonomy, and capture hooks (Git + Cursor). Stewardship of thinking, not transcript mining. Convention + bundle for teams using AI." \
  --homepage "https://scalefreestrategy.com" \
  --add-topic knowledge-management --add-topic documentation --add-topic developer-tools \
  --add-topic ai --add-topic cursor --add-topic git --add-topic adr \
  --add-topic reasoning --add-topic organizational-learning
```

Adjust **`--homepage`** if you prefer a docs URL or omit the flag.

## License

The repo root **`LICENSE`** is **MIT**. In **Settings** → **General**, set **License** to **MIT** if GitHub does not detect it automatically after push.

## Release

Create a **GitHub Release** from the latest tag (e.g. **`v1.1.0`**); paste or adapt the matching section from [CHANGELOG.md](../CHANGELOG.md). **New adopters** should pin **`v1.1.0`** or newer in `.calyx/core` (see [new-project.md](new-project.md)).

## Traffic and stats (what GitHub shows)

| Signal | Where | Notes |
|--------|--------|--------|
| **Clones** (unique cloners, traffic) | Repo **Insights** → **Traffic** | Visible to users with **maintainer/admin** access. Approximate; **not** a public “download counter.” |
| **Visitors** | **Insights** → **Traffic** | Page views on the GitHub UI; same access gate. |
| **Stars / forks** | Repo header | Public; rough interest proxy, not usage. |
| **Release assets** | Per-release download counts | Only if you attach **binaries**; **calyx-core** is source-only, so there are usually **no** release ZIP counts. |
| **`git` / submodule checkouts** | — | GitHub does **not** expose per-clone analytics for arbitrary `git clone` the way an app store does. Teams pin **tags**; you infer adoption from issues/PRs and your own telemetry if you add it. |

There is **no** built-in “Calyx downloads” metric. For a lightweight public signal, watch **Traffic** periodically or use the **GitHub API** (`/repos/{owner}/{repo}/traffic/clones`) with a token that has repo access—still **approximate** and **private** to the repo.
