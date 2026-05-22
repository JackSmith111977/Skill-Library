# Inversion Pattern Guide

Complete reference for creating inversion workflow skills.

## Concept

Inversion = Agent interviews user before executing. Unlike pipeline (linear, fixed steps), inversion needs upfront clarification because the task depends on user input.

Common use cases: research, investigation, code review with preferences, document creation with custom requirements.

## Structure

```
Phase 1: Information gathering (interview user)
    ↓
STAGE_GATE: HALT, output summary, wait for confirmation
    ↓
Phase 2: Execute (use collected info + atomic skills)
```

## Full example

```markdown
---
name: research-investigator
description: >-
  This skill should be used when the user asks to "research a topic",
  "investigate a problem", "look into a subject", or "find information about".
version: 1.0.0
allowed-tools: [Read, Bash, WebFetch]
metadata:
  pack: retrieval
  type: workflow
  design-pattern: inversion
  skill-type: technical
---

# research-investigator

Researches a topic by first understanding what user needs, then conducting targeted research.

## Phase 1: Understand research scope

Interview user to clarify:

- What specific topic or question to research?
- What depth needed? (quick overview / detailed analysis / exhaustive)
- Any preferred sources? (official docs, academic papers, news)
- Specific aspects to focus on?
- Format for results? (brief summary, structured report, comparison table)

Collect answers and synthesize into research brief.

---

## STAGE_GATE

Stop here. Present research brief to user:

```
## Research brief

**Topic**: [what user specified]
**Depth**: [quick / detailed / exhaustive]
**Focus areas**: [aspects to investigate]
**Output format**: [how to present results]

---

Confirm scope and proceed, or adjust research parameters.
```

Wait for explicit user confirmation before proceeding to Phase 2.

---

## Phase 2: Execute research

Use gathered parameters to conduct research.

### Step 1: Search for information

Use **web-researcher** to find relevant sources.

Search with keywords derived from research brief. Collect top sources.

### Step 2: Extract and synthesize

Read each source, extract key findings, synthesize into cohesive answer.

Reference sources using: `[Source Title](url)`

### Step 3: Present results

Format results according to user's requested format.
```

## STAGE_GATE markers

Lint rule checks for these keywords in inversion skills:

| Must have | Description |
|-----------|-------------|
| STAGE_GATE | The gate marker text |
| HALT | Stop instruction text |
| Wait for user | Confirmation required before proceeding |

Each gate must:
1. Summarize what was gathered/decided
2. Ask user to confirm
3. Explicitly block proceeding without confirmation

## Common mistakes

| Mistake | Fix |
|---------|-----|
| No STAGE_GATE marker | Add explicit "STAGE_GATE" heading |
| Proceeding without confirmation | Add "Do NOT proceed without user confirmation" |
| Only one question | Inversion needs enough questions to clarify scope (3-5 minimum) |
| No atomic skill references | Each phase should reference same-pack atomic skills |
