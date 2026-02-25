---
version: 2.0.0
layer: 1
type: protocol
priority: standard
applies_to: "*"
---

# Autonomous Evolution Protocols

1. **Task Registration:** Before starting a background refactor, register the "Evolution Task" in `.agent/memory/evolution.md`.
2. **Incrementalism:** Never refactor an entire module at once. Apply changes in atomic steps (one function or class at a time).
3. **Regression Testing:** After every evolution step, you MUST run existing tests. If tests fail, ROLL BACK immediately.
4. **Rule Alignment:** The primary goal of evolution is to bring legacy code into compliance with the latest `.agent/rules/`.
