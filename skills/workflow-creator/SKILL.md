---
name: workflow-creator
description: >-
  This skill should be used when the user asks to "create a workflow skill",
  "create a pipeline", "create an inversion skill", "create a multi-step skill",
  "create a workflow", or "scaffold a workflow".
version: 1.0.0
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
metadata:
  pack: meta
  type: atomic
  design-pattern: generator
  skill-type: technical
---

# workflow-creator

Guide user through creating workflow skill (pipeline or inversion pattern). Workflow skills orchestrate multiple atomic skills in the same pack.

## Step 1: Choose workflow pattern

Ask user which pattern fits:

| Pattern | Use when | Structure |
|---------|----------|-----------|
| pipeline | Linear multi-step with fixed order | Step 1 → Step 2 → Step 3, each step references atomic skill |
| inversion | Need user input before executing | Interview phase → STAGE_GATE → Execute phase |

**pipeline**: good for data processing, document generation, multi-stage review.
**inversion**: good for research, investigation, any task needing upfront clarification.

## Step 2: Check pack atomic skills

Workflow **must** reference atomic skills that exist in the same pack.

Check `skills/<pack>/` directory. Identify which atomic skills the workflow will reference. If needed atomic skills do not exist, create them first using skill-creator.

## Step 3: Create directory

Path: `skills/<pack>/<workflow-name>/`

```
skills/<pack>/<workflow-name>/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

## Step 4: Write SKILL.md frontmatter

```yaml
---
name: <workflow-name>         # kebab-case
description: >                # third person with trigger phrases
  This skill should be used when...
version: 1.0.0
allowed-tools: [Read, Bash]   # tools needed by the workflow
---
```

Same frontmatter rules as atomic skills. The metadata section is optional but recommended.

## Step 5: Write body — Pipeline pattern

Pipeline steps must be sequential with contiguous numbering.

**Format**:

```markdown
# <workflow-name>

One-liner describing what this pipeline does.

## Steps

### Step 1: <step-name>

Use <atomic-skill-name> to [action].

[Specific instructions for this step.]

### Step 2: <step-name>

Use <another-atomic-skill> to [action].

[Specific instructions for this step.]
```

**Rules**:
- Step numbering must start at 1, be contiguous (no gaps like 1, 2, 5)
- Each step must reference an existing atomic skill in the same pack
- Steps run sequentially — each step output feeds the next
- No circular dependencies between steps

See `references/pipeline-pattern.md` for complete example.

## Step 6: Write body — Inversion pattern

Inversion follows: interview → gate → execute.

**Format**:

```markdown
# <workflow-name>

One-liner describing what this inversion skill does.

## Phase 1: Information gathering

Interview user to collect all needed information.

### Questions to ask

- Question 1?
- Question 2?

### STAGE_GATE

**HALT** after gathering information. Output summary of what was collected. Ask user to confirm before proceeding.

Do NOT proceed to Phase 2 without explicit user confirmation.

## Phase 2: Execute

Use the collected information to perform the task.

Use <atomic-skill-name> to [action].
```

**STAGE_GATE rules**:
- Must explicitly halt and wait for user confirmation
- Must output a summary of what was collected
- Use clear marker text: `STAGE_GATE` or `HALT`
- Lint rule will check for these markers

See `references/inversion-pattern.md` for complete example.

## Step 7: Verify

Lint checks 4 additional workflow rules:

```bash
cd <project-root>
skill-manager lint skills/<pack>/<workflow-name>
```

| # | Rule | What it checks |
|---|------|---------------|
| 1 | Referenced atomic skill exists | All referenced skills must be in the same pack |
| 2 | Step numbering complete | Pipeline steps must be sequential, no gaps |
| 3 | STAGE_GATE markers present | Inversion must have explicit gate markers |
| 4 | No circular dependencies | Steps cannot form cycles |

**Must pass** (score ≥ 100). If lint fails, fix issues and re-run.
