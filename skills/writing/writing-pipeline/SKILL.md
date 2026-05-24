---
name: writing-pipeline
description: >
  This workflow should be used when the user wants to "write a
  complete article from scratch", "research and write about", "go from
  topic to finished draft", "produce a researched article", "run the
  full writing process", or "research, write, and polish an article".
  Chains research → writing → editing into a single pipeline.
version: 1.0.0
allowed-tools: [Read, Write, WebSearch, WebFetch, Grep]
metadata:
  pack: writing
  design-pattern: pipeline
  skill-type: workflow
  author: Kei
---

# Writing Pipeline

End-to-end writing workflow: research → draft → edit. Produces polished article from topic input.

## Purpose

Orchestrate three atomic skills into single coherent workflow. Each step consumes previous step's output. Quality gates between stages prevent cascading issues.

## Steps

### Step 1: Research (@research-assistant)

Run research-assistant with user's topic input.

**Input handoff**: User provides topic (+ optional depth, sources, constraints).
**Output**: Research brief with `<!-- research-brief -->` marker.
**Gate**: Research brief must have at least 2 sources cited. If not, loop back to gather more.

```
STAGE_GATE: Research brief complete? [yes/no]
- yes → proceed to Step 2
- no → return to research-assistant with gap description
```

### Step 2: Write Article (@article-writer)

Run article-writer consuming Step 1 output.

**Input handoff**: Topic + research brief (`<!-- research-brief -->` format).
**Output**: Article draft with section headings.
**Gate**: Article has clear thesis, 3+ body sections, and conclusion. Missing elements → return for revision.

```
STAGE_GATE: Article draft complete with thesis + 3 sections? [yes/no]
- yes → proceed to Step 3
- no → return to article-writer with gap description
```

### Step 3: Copy Edit (@copy-editor)

Run copy-editor consuming Step 2 output.

**Input handoff**: Article draft.
**Output**: Edit report with `<!-- edit-report -->` marker.
**Gate**: No critical errors. Major errors must be resolved (either apply suggestion or explicitly defer).

```
STAGE_GATE: Critical errors = 0? Major errors resolved? [yes/no]
- yes → pipeline complete, deliver final article + edit report
- no → apply critical fixes, re-edit
```

## Completion

Deliver to user:
1. Final article (clean)
2. Edit report (for reference)
3. Optional: original research brief

## Validation

- [ ] Step 1 output has `<!-- research-brief -->` marker
- [ ] Step 2 output has section headings and thesis
- [ ] Step 3 output has `<!-- edit-report -->` marker
- [ ] All stage gates passed
- [ ] No critical errors in final output
