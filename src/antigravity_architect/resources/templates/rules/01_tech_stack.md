---
version: 2.0.0
layer: 1
type: protocol
priority: mandatory
applies_to: "*"
---

# Tech Stack Protocol

1. **Detection:** Always identify the primary language and framework from `pyproject.toml`, `package.json`, or similar.
2. **Conventions:** Follow language-specific idiomatic patterns (e.g., PEP 8 for Python, Airbnb for JS).
3. **Ecosystem:** Prefer established libraries within the detected stack over custom solutions.
