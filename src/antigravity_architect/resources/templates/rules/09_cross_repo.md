---
version: 2.0.0
layer: 1
type: context
priority: standard
applies_to: "*"
---

# Multi-Repo Context Bridge

1. **Sister Repositories:** Refer to `context/links.md` for a list of related repositories in the same scratch space.
2. **Knowledge Sharing:** You are authorized to read `.agent/rules/` and `docs/TECH_STACK.md` from linked repositories to ensure architectural consistency.
3. **Dependency Mapping:** If a linked repository is a dependency (e.g., a shared library), prioritize its interface definitions over assumptions.
4. **No Mutation:** You may READ from sister repos, but never WRITE to them unless explicitly instructed to perform a cross-repo refactor.
