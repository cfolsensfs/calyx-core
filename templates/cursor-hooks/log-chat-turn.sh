#!/usr/bin/env bash
# Cursor command hook: append turns to workspace local/chat-log/ (see log_chat_turn.py).
# Install: copy this folder into .cursor/hooks/ and merge hooks.example.json into .cursor/hooks.json
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$DIR/log_chat_turn.py"
