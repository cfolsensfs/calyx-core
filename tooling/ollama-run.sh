#!/usr/bin/env bash
# Lean local runner: pipe context into Llama (or other) via Ollama.
# Usage: ./ollama-run.sh ../prompts/librarian.txt ./context-notes.md
set -euo pipefail
PROMPT_FILE="${1:?prompt file}"
CONTEXT_FILE="${2:-/dev/stdin}"
MODEL="${CALYX_OLLAMA_MODEL:-llama3}"
PROMPT="$(cat "$PROMPT_FILE")"
CONTEXT="$(cat "$CONTEXT_FILE")"
exec ollama run "$MODEL" "$(printf '%s\n\n---\n\n%s' "$PROMPT" "$CONTEXT")"
