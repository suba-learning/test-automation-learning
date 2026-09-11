#!/bin/bash
# Generate today's learning task into logs/<today>.md via Claude Code.
# Safe to rerun: skips if today's log already exists, and a failed Claude
# call leaves no log file behind.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/env.sh"
cd "$REPO_DIR"

TODAY="$(date +%F)"
LOG="logs/$TODAY.md"

if [ -f "$LOG" ]; then
  exit 0
fi

mkdir -p logs

PROMPT_FILE="$(mktemp)"
TITLE_FILE="$(mktemp)"
ERR_FILE="$(mktemp)"
OUTPUT_FILE="$(mktemp)"
trap 'rm -f "$PROMPT_FILE" "$TITLE_FILE" "$ERR_FILE" "$OUTPUT_FILE"' EXIT

if ! "$PYTHON_BIN" "$REPO_DIR/scripts/build_daily_prompt.py" \
      "$REPO_DIR/curriculum.yaml" "$REPO_DIR/state.json" "$PROMPT_FILE" "$TITLE_FILE" 2>"$ERR_FILE"; then
  cat "$ERR_FILE" >&2
  osascript -e 'display notification "Could not build today'\''s prompt — check logs/launchd-generate.log" with title "Daily Learning: generation failed"' >/dev/null 2>&1
  exit 1
fi

PROMPT="$(cat "$PROMPT_FILE")"
TITLE="$(cat "$TITLE_FILE")"
TITLE_ESCAPED="$(printf '%s' "$TITLE" | sed 's/\\/\\\\/g; s/"/\\"/g')"

if "$CLAUDE_BIN" -p "$PROMPT" > "$OUTPUT_FILE" 2>&1 && [ -s "$OUTPUT_FILE" ]; then
  TOPIC_ID="$("$PYTHON_BIN" -c "import json; print(json.load(open('state.json'))['current_topic_id'])")"
  ATTEMPT="$("$PYTHON_BIN" -c "import json; print(json.load(open('state.json'))['attempt_in_topic'])")"
  {
    echo "<!-- topic_id: $TOPIC_ID attempt: $ATTEMPT date: $TODAY -->"
    cat "$OUTPUT_FILE"
  } > "$LOG"
  osascript -e "display notification \"$TITLE_ESCAPED\" with title \"Daily Learning: today's task is ready\"" >/dev/null 2>&1
else
  cat "$OUTPUT_FILE" >&2
  osascript -e 'display notification "Claude call failed — check logs/launchd-generate.log" with title "Daily Learning: generation failed"' >/dev/null 2>&1
  exit 1
fi
