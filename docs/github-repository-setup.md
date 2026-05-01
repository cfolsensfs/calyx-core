# GitHub repository setup (first public release)

Use this after the **`v1.0.0`** tag is pushed. **Description and topics** can be set in the GitHub UI (**Settings** or the gear on the repo **About** sidebar) or with **`gh`** (see below).

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

Create a **GitHub Release** from tag **`v1.0.0`**; paste or adapt the **v1.0.0** section from [CHANGELOG.md](../CHANGELOG.md).
