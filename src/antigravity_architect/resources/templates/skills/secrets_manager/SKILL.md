---
name: secrets_manager
description: Handle API keys.
depends_on: ["env_context"]
---

# Secrets Skill

**Action:** Detect secrets in code. Move them to `.env`. Replace with `os.getenv()`.
