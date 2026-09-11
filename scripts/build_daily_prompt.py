#!/usr/bin/env python3
"""Build today's daily-task prompt from curriculum.yaml + state.json.

Usage: build_daily_prompt.py <curriculum.yaml> <state.json> <prompt_out> <title_out>
Exits non-zero (with a message on stderr) if current_topic_id has no match
in curriculum.yaml.
"""
import sys
import json
import yaml

curriculum_path, state_path, prompt_out, title_out = sys.argv[1:5]

with open(state_path) as f:
    state = json.load(f)

with open(curriculum_path) as f:
    curriculum = yaml.safe_load(f)

topic_id = state["current_topic_id"]
attempt = state["attempt_in_topic"]

topic = next((t for t in curriculum["topics"] if t["id"] == topic_id), None)
if topic is None:
    print(f"ERROR: topic id '{topic_id}' not found in curriculum.yaml "
          f"(curriculum may be complete, or state.json is out of sync)", file=sys.stderr)
    sys.exit(1)

target = curriculum.get("target", {})

resources = topic.get("resources") or []
resources_str = "\n".join(f"- {r}" for r in resources) if resources else "(none listed)"

known_bugs = target.get("known_bugs") or []
known_bugs_str = "\n".join(f"- {b}" for b in known_bugs) if known_bugs else "(none listed)"

prompt = f"""You are generating ONE day's learning task for a daily API test automation / system design tracker.

Target application:
- Name: {target.get('name', '')}
- Repo: {target.get('repo', '')}
- Known bugs (active in "Buggy Mode"):
{known_bugs_str}

Today's topic:
- id: {topic_id}
- track: {topic.get('track', '')}
- title: {topic.get('title', '')}
- goal: {topic.get('goal', '')}
- attempt number: {attempt} of task_budget {topic.get('task_budget', '?')}
- resources (use ONLY these URLs, never invent or guess a link):
{resources_str}

Write the response in Markdown with EXACTLY these sections, in this order, using these exact headings:

## Topic
State the topic id, the title, and the attempt number.

## Learn
A mechanistic concept explanation of about 300 words, with one concrete analogy. Only reference or link URLs from the resources list above — never invent links.

## Task
Exactly ONE task, scoped strictly to today's topic, completable in 30-60 minutes, using {target.get('name', 'the target app')} ({target.get('repo', '')}) as the practice target. If the attempt number is greater than 1, this task MUST go deeper than an earlier attempt would have (assume prior attempts already covered the basics of this topic) — do not repeat the same task.

## Done When
An unambiguous checklist. It MUST end with a git commit in this repo (test-automation-learning) whose commit message contains the topic id "{topic_id}". Code written for this task goes under exercises/{topic_id}/ in this repo. If the actual hands-on work happens in the {target.get('name', 'target')} repo instead, the final "done" step is committing a short note here under exercises/{topic_id}/ linking to that commit, with a commit message that still contains "{topic_id}".

## Notes
Leave the body of this section empty.

Output ONLY the Markdown for these five sections — no preamble, no postscript, no code fences around the whole thing.
"""

with open(prompt_out, "w") as f:
    f.write(prompt)

with open(title_out, "w") as f:
    f.write(topic.get("title", topic_id))
