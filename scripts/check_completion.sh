#!/bin/bash
# Check whether today's topic was completed (a matching git commit exists),
# advance state.json accordingly, and commit the state update.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/env.sh"
cd "$REPO_DIR"

TODAY="$(date +%F)"
LOG="logs/$TODAY.md"

ALREADY="$("$PYTHON_BIN" -c "
import json
state = json.load(open('state.json'))
today = '$TODAY'
print('yes' if any(h.get('date') == today for h in state.get('history', [])) else 'no')
")"
if [ "$ALREADY" = "yes" ]; then
  exit 0
fi

if [ ! -f "$LOG" ]; then
  osascript -e 'display notification "No task was generated today — nothing to check" with title "Daily Learning"' >/dev/null 2>&1
  exit 0
fi

TOPIC_ID="$(head -n 1 "$LOG" | sed -n 's/.*topic_id: \([^ ]*\).*/\1/p')"

if [ -z "$TOPIC_ID" ]; then
  osascript -e 'display notification "Could not read topic id from today'\''s log" with title "Daily Learning: check failed"' >/dev/null 2>&1
  exit 1
fi

COMMIT_LINE="$(git log --since="today 00:00" --grep="$TOPIC_ID" --format="%H %s" \
  | grep -v -E '^[0-9a-f]+ (chore:|docs:)' | head -n 1 || true)"

if [ -z "$COMMIT_LINE" ]; then
  osascript -e "display notification \"No commit found yet for $TOPIC_ID — still time to commit today\" with title \"Daily Learning: not done yet\"" >/dev/null 2>&1
  exit 0
fi

SHA="$(printf '%s' "$COMMIT_LINE" | awk '{print $1}')"
SUBJECT="$(printf '%s' "$COMMIT_LINE" | cut -d' ' -f2-)"

ATTEMPT="$("$PYTHON_BIN" -c "import json; print(json.load(open('state.json'))['attempt_in_topic'])")"

MASTERED=0
case "$SUBJECT" in
  *#mastered*) MASTERED=1 ;;
esac

"$PYTHON_BIN" "$REPO_DIR/scripts/advance_state.py" curriculum.yaml state.json "$TOPIC_ID" "$ATTEMPT" "$SHA" "$TODAY" "$MASTERED"

git add state.json "$LOG"
git commit -m "chore: advance state after $TOPIC_ID ($TODAY)" >/dev/null

if git remote get-url origin >/dev/null 2>&1; then
  if ! git push >/dev/null 2>&1; then
    osascript -e 'display notification "git push failed — push manually when you get a chance" with title "Daily Learning: push failed"' >/dev/null 2>&1
  fi
fi

NEXT_TITLE="$("$PYTHON_BIN" -c "
import json, yaml
state = json.load(open('state.json'))
curriculum = yaml.safe_load(open('curriculum.yaml'))
tid = state['current_topic_id']
t = next((x for x in curriculum['topics'] if x['id'] == tid), None)
print(t['title'] if t else tid)
")"
NEXT_TITLE_ESCAPED="$(printf '%s' "$NEXT_TITLE" | sed 's/\\/\\\\/g; s/"/\\"/g')"
osascript -e "display notification \"Nice work on $TOPIC_ID. Next up: $NEXT_TITLE_ESCAPED\" with title \"Daily Learning: completed\"" >/dev/null 2>&1

if [ "$(date +%u)" = "7" ]; then
  "$SCRIPT_DIR/generate_weekly_summary.sh"
fi
