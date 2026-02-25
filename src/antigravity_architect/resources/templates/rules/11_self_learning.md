---
version: 3.0.0
layer: 1
type: protocol
priority: high
applies_to: "*"
---

# Self-Learning & Autonomic Compaction <!-- ID: self_learning -->

## 1. Internalizing Lessons <!-- ID: lessons -->

Every interaction is an opportunity for the agent to refine its understanding of the project.

1. **Bug Discovery**: When a bug is found, document the root cause and a "Prevention Rule" in the appropriate rule file.
2. **Pattern Synthesis**: If a repeating pattern is observed, log it in `scratchpad.md` for future inclusion in the core Architect templates.
3. **Environment Quirks**: Document any OS-specific or tool-specific quirks encountered in `.agent/rules/01_tech_stack.md`.

## 2. Using the Knowledge Discovery System <!-- ID: knowledge_discovery -->

1. **KI Alignment**: Before starting research, always check existing Knowledge Items (KIs) provided at conversation start.
2. **KI Enrichment**: If a task reveals deep insights, prepare a summary to enrich the project's permanent knowledge base.

## 3. Persistent Memory Files <!-- ID: memory_files -->

The `.agent/memory/` directory is the authoritative source for the agent's "state of mind".

* **scratchpad.md**: Short-term focus, current task list, and immediate roadmap.
* **evolution.md**: Long-term technical debt and architectural goals.

## 4. Autonomic Compaction Protocol (v3.0) <!-- ID: compaction_protocol -->

To maintain context efficiency, the agent MUST periodically compact its memory files.

1. **Trigger**: When `scratchpad.md` exceeds 100 lines or 10 completed tasks.
2. **Action**:
    * Summarize completed tasks into a high-level "History" block.
    * Consolidate related sub-tasks into single lines.
    * Purge resolved blockers and stale research notes.
3. **Goal**: Ensure active context remains high-signal and low-token.

## 5. Main Script Evolution

The agent must proactively plan for the next iteration of the `antigravity-architect` package.

1. **Shadow Roadmap**: Maintain a list of "Pending Script Enhancements" in `evolution.md`.
2. **Constraint Enforcement**: Ensure any new patterns balance "Agentic Autonomy" with "Human Overridability".
