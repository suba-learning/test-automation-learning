#!/usr/bin/env python3
"""Apply one completion to state.json: append history, update streak, maybe advance topic.

Usage: advance_state.py <curriculum.yaml> <state.json> <topic_id> <attempt> <sha> <date YYYY-MM-DD> <mastered 0|1>
"""
import sys
import json
import yaml
from datetime import date as ddate, timedelta

curriculum_path, state_path, topic_id, attempt_str, sha, date_str, mastered_str = sys.argv[1:8]
attempt = int(attempt_str)
mastered_now = mastered_str == "1"

with open(state_path) as f:
    state = json.load(f)

with open(curriculum_path) as f:
    curriculum = yaml.safe_load(f)

topics = curriculum["topics"]
ids = [t["id"] for t in topics]
topic = next((t for t in topics if t["id"] == topic_id), None)
if topic is None:
    sys.exit(f"ERROR: topic id '{topic_id}' not found in curriculum.yaml")

state.setdefault("history", []).append({
    "date": date_str,
    "topic_id": topic_id,
    "attempt": attempt,
    "sha": sha,
})

today_d = ddate.fromisoformat(date_str)
last = state.get("last_completed_date")
if last:
    last_d = ddate.fromisoformat(last)
    if last_d == today_d - timedelta(days=1):
        state["streak_days"] = state.get("streak_days", 0) + 1
    else:
        state["streak_days"] = 1
else:
    state["streak_days"] = 1

state["longest_streak"] = max(state.get("longest_streak", 0), state["streak_days"])
state["last_completed_date"] = date_str

if mastered_now:
    state["mastered_early"] = True

task_budget = topic.get("task_budget", 1)
should_advance = attempt >= task_budget or state.get("mastered_early", False)

if should_advance:
    idx = ids.index(topic_id)
    if idx + 1 < len(ids):
        state["current_topic_id"] = ids[idx + 1]
    # else: already on the final topic — curriculum complete, stay put.
    state["attempt_in_topic"] = 1
    state["mastered_early"] = False
else:
    state["attempt_in_topic"] = attempt + 1

with open(state_path, "w") as f:
    json.dump(state, f, indent=2)
    f.write("\n")
