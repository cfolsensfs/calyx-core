#!/usr/bin/env bash
# Scaffold a new Cursor-friendly app repo: Calyx (.calyx + .cursorrules), git hints,
# and a default monorepo layout (web / api / mcp / shared / infra).
#
# Usage:
#   bash tooling/scaffold-cursor-app.sh /path/to/new-project
#   bash tooling/scaffold-cursor-app.sh . --name my-app
#
# Options:
#   --name <slug>     Human/project name for README (default: directory name)
#   --no-git          Do not run git init
#   --no-submodule    Do not add .calyx/core submodule (offline or core not on remote yet)
#   --minimal         Only Calyx + git files; no apps/web, apps/api, etc.
#   --force           Overwrite existing scaffold files if present
#
# Env:
#   CALYX_CORE_URL     Git URL for calyx-core (default: https://github.com/cfolsensfs/calyx-core.git)
#   SFS_SCAFFOLD=1     Set by create-sfs-workspace.sh; adds SFS badge lines in README / AGENTS.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(cd "${SCRIPT_DIR}/../templates/app-scaffold" && pwd)"
CURSOR_HOOKS_DIR="$(cd "${SCRIPT_DIR}/../templates/cursor-hooks" && pwd)"
CALYX_CORE_URL="${CALYX_CORE_URL:-https://github.com/cfolsensfs/calyx-core.git}"

TARGET=""
PROJECT_NAME=""
DO_GIT=1
DO_SUBMODULE=1
MINIMAL=0
FORCE=0

die() { echo "scaffold-cursor-app: $*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) PROJECT_NAME="${2:-}"; shift 2 ;;
    --no-git) DO_GIT=0; shift ;;
    --no-submodule) DO_SUBMODULE=0; shift ;;
    --minimal) MINIMAL=1; shift ;;
    --force) FORCE=1; shift ;;
    -h|--help)
      grep '^#' "$0" | head -40 | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      if [[ -z "${TARGET}" ]]; then
        TARGET="$1"
        shift
      else
        die "unexpected argument: $1"
      fi
      ;;
  esac
done

[[ -n "${TARGET}" ]] || die "usage: $0 /path/to/project [options]"

mkdir -p "${TARGET}"
TARGET="$(cd "${TARGET}" && pwd)"
[[ -d "${TEMPLATE_DIR}" ]] || die "missing template dir: ${TEMPLATE_DIR}"

if [[ -z "${PROJECT_NAME}" ]]; then
  PROJECT_NAME="$(basename "${TARGET}")"
fi

write_file() {
  local dest="$1"
  local src="$2"
  if [[ -e "${dest}" && "${FORCE}" -eq 0 ]]; then
    echo "skip (exists): ${dest}"
    return 0
  fi
  mkdir -p "$(dirname "${dest}")"
  cp "${src}" "${dest}"
  echo "wrote ${dest}"
}

replace_project_name() {
  local file="$1"
  if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' "s/__PROJECT_NAME__/${PROJECT_NAME}/g" "${file}"
  else
    sed -i "s/__PROJECT_NAME__/${PROJECT_NAME}/g" "${file}"
  fi
}

# Optional one-line badge under the title (e.g. Scale Free Strategy). Empty = remove placeholder line content.
replace_workspace_badge() {
  local file="$1"
  local badge=""
  if [[ "${SFS_SCAFFOLD:-}" == "1" ]]; then
    badge='> **SFS — Scale Free Strategy:** see `AGENTS.md` for how to record reasoning and ADRs in Calyx.'
  fi
  if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' "s#__WORKSPACE_BADGE__#${badge}#g" "${file}"
  else
    sed -i "s#__WORKSPACE_BADGE__#${badge}#g" "${file}"
  fi
}

# --- Root files ---
write_file "${TARGET}/.cursorrules" "${TEMPLATE_DIR}/cursorrules"
write_file "${TARGET}/.gitignore" "${TEMPLATE_DIR}/gitignore"
write_file "${TARGET}/.prettierrc.json" "${TEMPLATE_DIR}/prettierrc.json"
write_file "${TARGET}/.prettierignore" "${TEMPLATE_DIR}/prettierignore"
write_file "${TARGET}/.editorconfig" "${TEMPLATE_DIR}/editorconfig"

# --- Cursor hooks: local chat log (gitignored under local/chat-log/) ---
[[ -d "${CURSOR_HOOKS_DIR}" ]] || die "missing cursor-hooks templates: ${CURSOR_HOOKS_DIR}"
mkdir -p "${TARGET}/.cursor/hooks"
write_file "${TARGET}/.cursor/hooks/log_chat_turn.py" "${CURSOR_HOOKS_DIR}/log_chat_turn.py"
write_file "${TARGET}/.cursor/hooks/log-chat-turn.sh" "${CURSOR_HOOKS_DIR}/log-chat-turn.sh"
chmod +x "${TARGET}/.cursor/hooks/log-chat-turn.sh" "${TARGET}/.cursor/hooks/log_chat_turn.py"
write_file "${TARGET}/.cursor/hooks.json" "${CURSOR_HOOKS_DIR}/hooks.example.json"

write_file "${TARGET}/README.md" "${TEMPLATE_DIR}/README.md"
replace_project_name "${TARGET}/README.md"
replace_workspace_badge "${TARGET}/README.md"

write_file "${TARGET}/AGENTS.md" "${TEMPLATE_DIR}/AGENTS.md"
replace_project_name "${TARGET}/AGENTS.md"
replace_workspace_badge "${TARGET}/AGENTS.md"

write_file "${TARGET}/VERSION" "${TEMPLATE_DIR}/VERSION"

write_file "${TARGET}/SETUP_CALYX.md" "${TEMPLATE_DIR}/SETUP_CALYX.md"
replace_project_name "${TARGET}/SETUP_CALYX.md"

mkdir -p "${TARGET}/docs"
write_file "${TARGET}/docs/GIT.md" "${TEMPLATE_DIR}/docs-GIT.md"

mkdir -p "${TARGET}/.github/workflows"
write_file "${TARGET}/.github/workflows/calyx-verify.yml" "${TEMPLATE_DIR}/github-workflows-calyx-verify.yml"

# --- .calyx local layer ---
mkdir -p "${TARGET}/.calyx/reasoning" "${TARGET}/.calyx/decisions" "${TARGET}/.calyx/taxonomy"
write_file "${TARGET}/.calyx/README.md" "${TEMPLATE_DIR}/dot-calyx-README.md"
write_file "${TARGET}/.calyx/reasoning/_TEMPLATE.md" "${TEMPLATE_DIR}/reasoning-TEMPLATE.md"
write_file "${TARGET}/.calyx/decisions/ADR-TEMPLATE.md" "${TEMPLATE_DIR}/ADR-TEMPLATE.md"
write_file "${TARGET}/.calyx/taxonomy/local-tags.yaml" "${TEMPLATE_DIR}/local-tags.yaml"
write_file "${TARGET}/.calyx/AGENT_ROLES.md" "${SCRIPT_DIR}/../templates/project-agent-roles.md"

# --- Default app layout ---
if [[ "${MINIMAL}" -eq 0 ]]; then
  mkdir -p "${TARGET}/apps/web" "${TARGET}/apps/api" "${TARGET}/mcp" "${TARGET}/packages/shared" "${TARGET}/infra" "${TARGET}/local"
  write_file "${TARGET}/apps/web/README.md" "${TEMPLATE_DIR}/apps-web-README.md"
  write_file "${TARGET}/apps/api/README.md" "${TEMPLATE_DIR}/apps-api-README.md"
  write_file "${TARGET}/mcp/README.md" "${TEMPLATE_DIR}/mcp-README.md"
  write_file "${TARGET}/packages/shared/README.md" "${TEMPLATE_DIR}/packages-shared-README.md"
  write_file "${TARGET}/infra/README.md" "${TEMPLATE_DIR}/infra-README.md"
  # local/ is gitignored; optional placeholder for humans
  if [[ ! -f "${TARGET}/local/README.txt" ]] || [[ "${FORCE}" -eq 1 ]]; then
    mkdir -p "${TARGET}/local"
    echo "This folder is ignored by git. Put secrets, scratch files, and large dumps here." > "${TARGET}/local/README.txt"
    echo "wrote ${TARGET}/local/README.txt"
  fi
fi

# --- Git ---
if [[ "${DO_GIT}" -eq 1 ]]; then
  if [[ ! -d "${TARGET}/.git" ]]; then
    (cd "${TARGET}" && git init -b main)
    echo "git init main in ${TARGET}"
  else
    echo "git repo already present; skipping git init"
  fi
fi

if [[ "${DO_SUBMODULE}" -eq 1 ]]; then
  if [[ ! -d "${TARGET}/.git" ]]; then
    echo "warning: --no-git was not set but .git missing; skipping submodule add" >&2
  elif [[ -e "${TARGET}/.calyx/core/.git" ]] || [[ -f "${TARGET}/.calyx/core" ]]; then
    echo "skip submodule: .calyx/core already exists"
  else
    (cd "${TARGET}" && git submodule add "${CALYX_CORE_URL}" .calyx/core)
    echo "added submodule .calyx/core <- ${CALYX_CORE_URL}"
  fi
else
  echo "skip submodule (--no-submodule). Add later:"
  echo "  cd \"${TARGET}\" && git submodule add ${CALYX_CORE_URL} .calyx/core"
  echo "  then: bash .calyx/core/tooling/calyx-setup-capture.sh"
fi

if [[ "${DO_SUBMODULE}" -eq 1 ]] && [[ -d "${TARGET}/.git" ]]; then
  if [[ -e "${TARGET}/.calyx/core/.git" ]] || [[ -f "${TARGET}/.calyx/core" ]]; then
    (cd "${TARGET}" && git submodule update --init --recursive) || true
    SETUP="${TARGET}/.calyx/core/tooling/calyx-setup-capture.sh"
    if [[ -f "${SETUP}" ]]; then
      (cd "${TARGET}" && bash "${SETUP}")
    else
      echo "Note: calyx-setup-capture.sh not found yet — run it after submodule points at calyx-core v1+"
    fi
  fi
fi

echo
echo "Scaffold complete: ${TARGET}"
echo "Next: cd \"${TARGET}\" && git submodule update --init --recursive  (if submodule was not fully init)"
echo "Then open this folder as the workspace root in Cursor."
echo "Calyx v1 capture: git inbox stubs + local/chat-log (python3 on PATH; see .cursor/hooks.json)."
