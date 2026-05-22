# Pipeline Pattern Guide

Complete reference for creating pipeline workflow skills.

## Structure

Pipeline = linear sequence of steps, each invoking an atomic skill in the same pack.

```
Step 1: Validate input     (uses data-validator)
    ↓
Step 2: Transform data     (uses csv-processor)
    ↓
Step 3: Generate report    (uses report-generator)
    ↓
Step 4: Review output      (uses output-reviewer)
```

## Full example

```markdown
---
name: data-pipeline
description: >-
  This skill should be used when the user asks to "process data from start to finish",
  "run the full data pipeline", or "execute data workflow".
version: 1.0.0
allowed-tools: [Read, Bash, Write]
metadata:
  pack: data
  type: workflow
  design-pattern: pipeline
  skill-type: technical
---

# data-pipeline

Orchestrates full data processing workflow: validate, transform, report, review.

## Steps

### Step 1: Validate input

Use **data-validator** to check input file format and schema.

Validate CSV column types, JSON schema, and required fields. Report any format errors to user. Halt if validation fails.

### Step 2: Transform data

Use **csv-processor** to apply transformations.

Clean data, normalize formats, compute derived fields. Output transformed file to `output/transformed.csv`.

### Step 3: Generate report

Use **report-generator** to create summary report.

Read transformed data, compute aggregates (row count, sum, average by group). Write report to `output/report.md`.

### Step 4: Review output

Use **output-reviewer** to check final output quality.

Verify report completeness, check data consistency, flag anomalies. Present summary to user.
```

## Lint requirements

Pipeline must pass these workflow lint rules:

| Rule | Requirement |
|------|------------|
| Step completeness | Steps numbered 1, 2, 3... contiguous, no gaps |
| Atomic skill existence | Each step's referenced skill exists in `skills/<pack>/` |
| No circular deps | Steps A→B→C, never A→B→A |

## Common mistakes

| Mistake | Why it fails | Fix |
|---------|-------------|-----|
| Skipping step numbers | Lint detects gaps (1, 2, 5) | Renumber sequentially |
| Referencing nonexistent skill | Lint checks file existence | Create skill or remove reference |
| Mixing packs | Workflow can only reference same-pack skills | Move skills to correct pack |
| Duplicate step numbers | Same number used twice | Check numbering |
