#!/bin/bash
# Generate summaries/<YYYY-Www>.md from the last 7 days of history and commit it.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/env.sh"
cd "$REPO_DIR"

WEEK="$(date +%G-W%V)"
OUT="summaries/$WEEK.md"
mkdir -p summaries

PROMPT_FILE="$(mktemp)"
ERR_FILE="$(mktemp)"
OUTPUT_FILE="$(mktemp)"
trap 'rm -f "$PROMPT_FILE" "$ERR_FILE" "$OUTPUT_FILE"' EXIT

if ! "$PYTHON_BIN" "$REPO_DIR/scripts/build_weekly_prompt.py" curriculum.yaml state.json "$WEEK" "$PROMPT_FILE" 2>"$ERR_FILE"; then
  cat "$ERR_FILE" >&2
  osascript -e 'display notification "Could not build weekly summary prompt" with title "Weekly Summary: failed"' >/dev/null 2>&1
  exit 1
fi

PROMPT="$(cat "$PROMPT_FILE")"

if "$CLAUDE_BIN" -p "$PROMPT" > "$OUTPUT_FILE" 2>&1 && [ -s "$OUTPUT_FILE" ]; then
  cp "$OUTPUT_FILE" "$OUT"
  git add "$OUT"
  git commit -m "docs: weekly summary $WEEK" >/dev/null

  if git remote get-url origin >/dev/null 2>&1; then
    if ! git push >/dev/null 2>&1; then
      osascript -e 'display notification "git push failed for weekly summary" with title "Weekly Summary: push failed"' >/dev/null 2>&1
    fi
  fi
  osascript -e "display notification \"Weekly summary for $WEEK is ready\" with title \"Daily Learning: weekly summary\"" >/dev/null 2>&1
else
  cat "$OUTPUT_FILE" >&2
  osascript -e 'display notification "Weekly summary generation failed" with title "Weekly Summary: failed"' >/dev/null 2>&1
  exit 1
fi
