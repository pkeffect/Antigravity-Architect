---
version: 2.0.0
layer: 1
type: protocol
priority: mandatory
applies_to: "*"
---

# Security Protocols

1. **Secrets:** Never output API keys. Use `.env`.
2. **Inputs:** Validate all inputs.
3. **Dependencies:** Warn if using deprecated libraries.
