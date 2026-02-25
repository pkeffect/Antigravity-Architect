---
version: 2.0.0
layer: 0
type: safety
priority: mandatory
applies_to: "*"
---

# Environment & OS Awareness

1. **Dynamic OS Detection:** Run `python .agent/skills/env_context/env_context.py` to dynamically detect your OS (Windows/Linux/macOS) and shell environment. Adjust your commands accordingly (e.g. use PowerShell over bash on Windows, avoid `grep`/`ls`/`cat` on Windows CMD).
2. **Localizing Environments:** ALWAYS use the python interpreter located at `.\.venv\Scripts\python.exe` (Windows) or `./.venv/bin/python` (Linux). Before running tests or scripts, ensure the environment is activated.
3. **Docker Sandboxing:** If `.devcontainer` is present or `SANDBOX_TYPE=docker` is set, you are isolated in a Linux container. Your shell commands should be formatted for a Linux sandbox.
