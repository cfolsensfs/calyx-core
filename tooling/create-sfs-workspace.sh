#!/usr/bin/env bash
# Scale Free Strategy (SFS) — create a new workspace under ~/Documents/CURSOR (by default),
# with Calyx scaffold, VERSION 0.1, AGENTS.md, initial git commit, and GitHub repo + push via gh.
#
# Usage:
#   bash tooling/create-sfs-workspace.sh "Human Project Name" [repo-slug]
#
# The repo-slug is also the on-disk folder name under SFS_WORKSPACE_ROOT (default
# ~/Documents/CURSOR/<slug>). Slug must be all lowercase [a-z0-9-]+ — same spelling
# you want on GitHub (GitHub treats names case-insensitively; use lowercase everywhere).
#
# Options:
#   --public           Create a public GitHub repo (default: private)
#   --no-github        Do not run gh; only scaffold + local commit
#   --no-submodule     Pass through to scaffold (offline / no network)
#   --root <path>      Parent folder for the new project (default: $SFS_WORKSPACE_ROOT or ~/Documents/CURSOR)
#   --dry-run          Print actions only
#
# Requires: git. For GitHub automation: GitHub CLI (`gh`) and `gh auth login`.
#
# Env:
#   SFS_WORKSPACE_ROOT   Default parent directory (default: $HOME/Documents/CURSOR)
#   GITHUB_OWNER         GitHub user or org for new repo (default: cfolsensfs)
#   CALYX_CORE_URL       Passed to scaffold (submodule URL)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAFFOLD="${SCRIPT_DIR}/scaffold-cursor-app.sh"

SFS_WORKSPACE_ROOT="${SFS_WORKSPACE_ROOT:-${HOME}/Documents/CURSOR}"
GITHUB_OWNER="${GITHUB_OWNER:-cfolsensfs}"
VISIBILITY="--private"
DO_GITHUB=1
DO_SUBMODULE=( )
ROOT_OVERRIDE=""
DRY_RUN=0
POSITIONAL=()

die() { echo "create-sfs-workspace: $*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --public) VISIBILITY="--public"; shift ;;
    --no-github) DO_GITHUB=0; shift ;;
    --no-submodule) DO_SUBMODULE=( "--no-submodule" ); shift ;;
    --root) ROOT_OVERRIDE="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help)
      grep '^#' "$0" | head -35 | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      POSITIONAL+=( "$1" ); shift ;;
  esac
done

[[ ${#POSITIONAL[@]} -ge 1 ]] || die "usage: $0 \"Project Name\" [repo-slug] [options]"
PROJECT_NAME="${POSITIONAL[0]}"
SLUG="${POSITIONAL[1]:-}"

slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed -e 's/[^a-z0-9]/-/g' -e 's/--*/-/g' -e 's/^-//' -e 's/-$//'
}

[[ -n "${SLUG}" ]] || SLUG="$(slugify "${PROJECT_NAME}")"
[[ "${SLUG}" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "invalid slug \"${SLUG}\" — use lowercase letters, digits, hyphens only"

PARENT="${ROOT_OVERRIDE:-${SFS_WORKSPACE_ROOT}}"
TARGET="${PARENT%/}/${SLUG}"

[[ -e "${SCAFFOLD}" ]] || die "missing scaffold: ${SCAFFOLD}"

run() {
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "Would create: ${TARGET}"
  echo "Project name: ${PROJECT_NAME}"
  echo "GitHub repo:  ${GITHUB_OWNER}/${SLUG} (${VISIBILITY#--})"
  run mkdir -p "${PARENT}"
  run env SFS_SCAFFOLD=1 bash "${SCAFFOLD}" "${TARGET}" --name "${PROJECT_NAME}" "${DO_SUBMODULE[@]:-}"
  run git -C "${TARGET}" add -A
  run git -C "${TARGET}" commit -m "chore: initial SFS workspace for ${PROJECT_NAME} (v0.1)"
  if [[ "${DO_GITHUB}" -eq 1 ]]; then
    run gh repo create "${GITHUB_OWNER}/${SLUG}" ${VISIBILITY} --source="${TARGET}" --remote=origin --push
  fi
  exit 0
fi

mkdir -p "${PARENT}"
[[ ! -e "${TARGET}" ]] || die "path already exists: ${TARGET}"

echo "Creating SFS workspace at ${TARGET}"

SFS_SCAFFOLD=1 bash "${SCAFFOLD}" "${TARGET}" --name "${PROJECT_NAME}" "${DO_SUBMODULE[@]:-}"

if [[ ! -d "${TARGET}/.git" ]]; then
  die "scaffold did not create a git repo (unexpected)"
fi

git -C "${TARGET}" add -A

if ! git -C "${TARGET}" diff --cached --quiet; then
  git -C "${TARGET}" commit -m "chore: initial SFS workspace for ${PROJECT_NAME} (v0.1)"
  echo "Created initial commit."
else
  echo "Nothing to commit (unexpected after scaffold)." >&2
fi

if [[ "${DO_GITHUB}" -eq 1 ]]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "GitHub CLI (gh) not found. Install: https://cli.github.com/" >&2
    echo "Then: cd \"${TARGET}\" && gh repo create ${GITHUB_OWNER}/${SLUG} ${VISIBILITY} --source=. --remote=origin --push" >&2
    echo >&2
    echo "Done (local only). Open this folder as the Cursor workspace root:" >&2
    echo "  ${TARGET}" >&2
    exit 0
  fi
  if gh repo view "${GITHUB_OWNER}/${SLUG}" >/dev/null 2>&1; then
    die "GitHub repo ${GITHUB_OWNER}/${SLUG} already exists — choose a different slug or delete the repo."
  fi
  gh repo create "${GITHUB_OWNER}/${SLUG}" ${VISIBILITY} --source="${TARGET}" --remote=origin --push
  echo "Remote: https://github.com/${GITHUB_OWNER}/${SLUG}"
else
  echo "Skipping GitHub (--no-github). When ready:"
  echo "  cd \"${TARGET}\" && gh repo create ${GITHUB_OWNER}/${SLUG} ${VISIBILITY} --source=. --remote=origin --push"
fi

echo
echo "Done. Open this folder as the Cursor workspace root:"
echo "  ${TARGET}"
