---
version: 2.0.0
layer: 0
type: safety
priority: mandatory
applies_to: "*"
---

# Workspace Boundary Enforcement <!-- ID: boundary_enforcement -->

1. **Absolute Path Restriction:** You are strictly forbidden from reading, writing, or executing anything outside of the current project root directory.
2. **Command Safety:** Before running any command, verify it does not attempt to access `../` or absolute system paths like `/etc/` or `C:\Windows\`.
3. **Environment Isolation:** Do not attempt to modify system-level configurations, install non-project global dependencies, or access files in other workspaces unless explicitly authorized.
4. **Data Integrity:** Never delete files or move them outside the project boundaries.

## 5. Repository Lifecycle States <!-- ID: lifecycle_states -->

1. **INIT**: The repository is being actively scaffolded. Agents should be flexible but cautious.
2. **STABLE**: Finalized architecture. Agents must follow strict ADR protocols and avoid breaking changes.
3. **ARCHIVED**: Read-only state. No modifications allowed without manual state transition.
