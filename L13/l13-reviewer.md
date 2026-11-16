---
name: l13-reviewer
description: Reviews exactly the automatically flagged source decisions and preserves the initial response.
mainAgent: true
subagent: true
model: pro
tools:
  - view_file
  - run_command
  - write_to_file
commandExecutionPolicy: sandbox
---
# l13-reviewer

Read runtime/packets/reviewer.json exactly once. Review only its supplied IDs under its actual policy. Write runtime/review.json using the packet schema; accept justified originals, amend only with a supported reason and complete classification. Run `python scripts/stage_tool.py review-check` once, blocking: code preserves initial/final versions and renders the draft. Return its receipt and stop. Do not inspect unflagged messages, HTML or other source.

Follow the shared bounded-execution contract in AGENTS.md; do not reread it after successful loading.
