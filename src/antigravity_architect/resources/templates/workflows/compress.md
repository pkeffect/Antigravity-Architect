---
trigger: /compress
---
# Memory Compression Workflow
1. Read `.agent/memory/scratchpad.md`.
2. Identify entries older than 7 days or 50 lines.
3. Summarize them into a 'Historical Digest' section.
4. Truncate the active log to keep the context window lean.
