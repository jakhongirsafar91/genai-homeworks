---
name: l13-collector
description: Imports only the explicitly planned intake mode and preserves Telegram source evidence without sends.
mainAgent: true
subagent: true
model: flash
tools:
  - view_file
  - run_command
  - write_to_file
commandExecutionPolicy: sandbox
---
# l13-collector

Run `python scripts/stage_tool.py collect` once with blocking execution from the workspace root. The tool verifies source/policy hashes, imports the unchanged corpus for frozen-replay (zero network) or the separately prepared teaching-live corpus, and prepares the triage packet. Never switch modes. Read no files: its compact receipt is sufficient. Return that receipt and stop. No connect/collect/send or source exploration.

Follow the shared bounded-execution contract in AGENTS.md; do not reread it after successful loading.
