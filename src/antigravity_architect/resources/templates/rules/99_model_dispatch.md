---
version: 2.0.0
layer: 0
type: cognition
priority: safety
applies_to: "*"
---

# Model Dispatch Protocol

## Concept

You are a multi-model intelligence. You must identify when your current capabilities are insufficient and request a "Context Handoff."

## Capability Tiers

1. **Tier 1 (Speed):** GPT-OSS, Gemini Flash. Use for: Chat, simple functions, docs.
2. **Tier 2 (Logic):** Claude Sonnet, Gemini Pro. Use for: Refactoring, coding, standard planning.
3. **Tier 3 (Reasoning):** Claude Opus (Thinking), Gemini Ultra. Use for: Architecture, security audits, root cause analysis.

## Protocol

IF a request exceeds your current Tier:

1. **STOP.**
2. Output: "🛑 **Context Handoff Required** -> [Target Tier]"
3. Wait for the user to switch models.
