#!/bin/bash
# Shared environment for all scripts in this repo.
# launchd runs jobs without your shell profile, so bare `claude` / `python3`
# are not found there — every script must source this file first and use
# $CLAUDE_BIN / $PYTHON_BIN.

CLAUDE_BIN="/Users/subanarayanan/.local/bin/claude"
PYTHON_BIN="/opt/homebrew/bin/python3"
REPO_DIR="/Users/subanarayanan/dev/test-automation-learning"
export PATH="$(dirname "$CLAUDE_BIN"):$(dirname "$PYTHON_BIN"):/usr/bin:/bin:/usr/sbin:/sbin"
unset ANTHROPIC_API_KEY   # force Claude Code subscription auth, never billed API
