#!/usr/bin/env python3
"""Build the weekly summary prompt from the last 7 days of state.json history.

Usage: build_weekly_prompt.py <curriculum.yaml> <state.json> <YYYY-Www> <prompt_out>
"""
import sys
import json
import yaml
from datetime import date, timedelta

curriculum_path, state_path, week_str, out_path = sys.argv[1:5]

with open(state_path) as f:
    state = json.load(f)

with open(curriculum_path) as f:
    curriculum = yaml.safe_load(f)

topics_by_id = {t["id"]: t for t in curriculum["topics"]}

cutoff = date.today() - timedelta(days=7)
recent = [h for h in state.get("history", []) if date.fromisoformat(h["date"]) > cutoff]

lines = []
for h in recent:
    t = topics_by_id.get(h["topic_id"], {})
    lines.append(
        f"- {h['date']}: {h['topic_id']} — {t.get('title', h['topic_id'])} "
        f"(attempt {h['attempt']}, commit {h['sha'][:7]})"
    )
history_block = "\n".join(lines) if lines else "(no completions recorded this week)"

next_id = state.get("current_topic_id")
next_topic = topics_by_id.get(next_id, {})
next_desc = f"{next_id} — {next_topic.get('title', '')}"

prompt = f"""Write a short "weekly small wins" summary in Markdown for a daily API test automation / system design learning log.

This week's completed topics (from the tracker's history, most recent last):
{history_block}

Current streak: {state.get('streak_days', 0)} days. Longest streak so far: {state.get('longest_streak', 0)} days.

Upcoming topic: {next_desc}

Write Markdown with EXACTLY these sections, using these exact headings:

## Week {week_str}
One short intro sentence, then a bullet list with one bullet per completed topic listed above, each with a one-line takeaway (what was actually learned or built — do not just restate the title).

## Streak
One or two sentences about the current streak ({state.get('streak_days', 0)} days) and the longest streak so far ({state.get('longest_streak', 0)} days).

## Next Week
One or two sentences naming the upcoming topic ({next_desc}) and briefly what it involves.

Output ONLY the Markdown for these sections — no preamble, no postscript.
"""

with open(out_path, "w") as f:
    f.write(prompt)
