# Git workflow for this repo

## Initial setup (new machine)

```bash
git clone --recurse-submodules <REPO-URL>.git
cd <repo>
```

If you cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

## Daily work

```bash
git checkout -b <branch-name>   # optional feature branch
# … edit …
git status
git add -A
git commit -m "Clear, complete sentence describing the change."
git push -u origin <branch-name>
```

## Calyx submodule pin

To move **calyx-core** to a newer commit on `main` (or a tag):

```bash
cd .calyx/core
git fetch origin
git checkout main && git pull   # or: git checkout v0.x.y
cd ../..
git add .calyx/core
git commit -m "Bump calyx-core pin"
git push
```

## Cursor

Open the **repository root** in Cursor so `.cursorrules` and `.calyx/` apply to the whole app.
