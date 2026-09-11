# test-automation-learning

A public, verifiable daily learning log for **API test automation frameworks**
and **system design**, practiced against my own app,
[api-bug-buddy](https://github.com/suba-learning/api-bug-buddy).

api-bug-buddy has a "Buggy Mode" that injects known bugs into its API
responses (see `target.known_bugs` in `curriculum.yaml`) — the point of this
tracker is to write tests and design test strategies that actually catch
those bugs, not just to read about testing theory.

## How it's verified

Nothing here is self-reported. Each day a script generates one concrete task
in `logs/`, and each evening a second script checks for a **git commit**
referencing that day's topic id before advancing the curriculum pointer in
`state.json`. If no commit is found, the day is simply not counted — the
curriculum doesn't move.

## Layout

- [`curriculum.yaml`](./curriculum.yaml) — the fixed, ordered syllabus (target
  app info + topics). Never reordered or edited by the scripts.
- [`state.json`](./state.json) — the current position in the curriculum,
  streaks, and full completion history.
- [`logs/`](./logs) — one Markdown file per day with that day's generated
  task.
- [`summaries/`](./summaries) — a short "weekly small wins" summary, written
  every Sunday.
- [`scripts/`](./scripts) — the generation/check/summary scripts, plus
  `env.sh` (shared tool paths, sourced by every script).
- [`exercises/`](./exercises) — code produced for each topic, one directory
  per topic id.
- [`launchd/`](./launchd) — reference launchd job definitions (not
  installed automatically — see that folder for activation steps).

## Current status

- Current topic: `fw-01` — see `state.json.current_topic_id`
- Streak: 0 days
- Longest streak: 0 days

(These are placeholders — `state.json` is the source of truth and updates
automatically as days are completed.)
