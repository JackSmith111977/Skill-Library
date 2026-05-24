---
name: content-research
description: >
  This workflow should be used when the user wants to "research
  something for content", "find material for a piece I'm writing",
  "gather research for content", "investigate a topic for an article",
  or needs structured research output but hasn't fully defined the
  scope. Interviews user first, then researches.
version: 1.0.0
allowed-tools: [Read, Write, WebSearch, WebFetch]
metadata:
  pack: writing
  design-pattern: inversion
  skill-type: workflow
  author: Kei
---

# Content Research

Interview-driven research workflow. Clarify user needs first, then execute targeted research. Prevents wasted research on misaligned scope.

## Purpose

Inversion pattern: ask before search. User often has partial understanding of what they need. Interview draws out real requirements, then research-assistant executes against clear brief.

## Steps

### Step 1: User Interview

Ask user structured questions to define research scope:

1. **Topic**: What subject? Broad or specific angle?
2. **Purpose**: Why need this research? (article / decision / presentation / background)
3. **Audience**: Who consumes this? (technical / general / executive)
4. **Depth**: Brief overview or deep dive?
5. **Sources**: Any preferred sources or ones to avoid?
6. **Deadline**: When needed? (affects depth)
7. **Known**: What already known? What gaps to fill?

Collect answers into structured research brief.

```
STAGE_GATE: User provided clear topic + purpose + depth? [yes/no]
- yes → proceed to Step 2
- no → ask clarifying questions until scope defined
```

### Step 2: Execute Research (@research-assistant)

Run research-assistant using interview output as input.

**Input handoff**: Structured brief from Step 1 (topic, depth, sources, constraints).
**Output**: Research brief with `<!-- research-brief -->` marker.

```
STAGE_GATE: Research brief answers all questions from interview? [yes/no]
- yes → deliver to user
- no → narrow query and re-run research on gap areas
```

## Completion

Deliver to user:
1. Research brief (structured, source-cited)
2. Interview summary (what user asked for)
3. Any gaps identified that need human judgment

## Validation

- [ ] Interview questions cover all 7 scope dimensions
- [ ] Research brief addresses each user requirement
- [ ] Sources cited per claim
- [ ] Gaps explicitly flagged
