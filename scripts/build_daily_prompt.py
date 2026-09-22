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

api_reference = target.get("api_reference") or []
def _fmt_endpoint(e):
    body = ", ".join(e.get("request_body") or []) or "(none)"
    return (f"- {e.get('method', '')} {e.get('path', '')} | auth: {e.get('auth', '')} "
            f"| body fields: {body} | success status: {e.get('success_status', '')}")
api_reference_str = "\n".join(_fmt_endpoint(e) for e in api_reference) if api_reference else "(none listed)"

prompt = f"""You are generating ONE day's learning task for a daily API test automation / system design tracker.

Target application:
- Name: {target.get('name', '')}
- Repo: {target.get('repo', '')}
- Base URL (use this as the API base URL in all code and commands — never localhost or a placeholder): {target.get('base_url', '')}
- API reference (current endpoints as implemented today):
{api_reference_str}
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
A code-along walkthrough, 15-20 minutes, that builds from an empty file. Break it into numbered steps. Each step adds ONE small concept, then shows: the exact code to type, the command to run it, the expected output (or expected error, then the fix), and one or two sentences on why it works. Start from the simplest working version and refactor toward the better design, rather than showing the final design first. Use only endpoints from the API reference above, never invented ones. Only reference or link URLs from the resources list above — never invent links.

## Task
A "now you try it" exercise, 30-45 minutes, that extends the walkthrough and is NOT solved by it. Scoped strictly to today's topic, using {target.get('name', 'the target app')} ({target.get('repo', '')}) as the practice target. If the attempt number is greater than 1, this task MUST go deeper than an earlier attempt would have (assume prior attempts already covered the basics of this topic) — do not repeat the same task.

## Done When
An unambiguous checklist. It MUST end with a git commit in this repo (test-automation-learning) whose commit message contains the topic id "{topic_id}". Code written for this task goes under exercises/{topic_id}/ in this repo. If the actual hands-on work happens in the {target.get('name', 'target')} repo instead, the final "done" step is committing a short note here under exercises/{topic_id}/ linking to that commit, with a commit message that still contains "{topic_id}".

## Interview Questions
3 questions a senior QA interview might ask on this topic. No answers.

## Notes
Leave the body of this section empty.

Output ONLY the Markdown for these six sections — no preamble, no postscript, no code fences around the whole thing.
"""

with open(prompt_out, "w") as f:
    f.write(prompt)

with open(title_out, "w") as f:
    f.write(topic.get("title", topic_id))
