# Frontmatter Reference

Complete guide to SKILL.md frontmatter fields for the Skill Library project.

## Required fields

### name

Skill identifier, used as command name and directory name.

```yaml
name: data-validator
```

| Rule | Constraint |
|------|-----------|
| Length | 1-64 characters |
| Charset | lowercase letters, digits, hyphens |
| Start | letter only |
| End | letter or digit |
| No consecutive hyphens | `my--skill` invalid |
| Must match directory name | `data-validator/` → `data-validator` |

### description

Trigger condition for the skill. What the user says that should activate this skill.

```yaml
description: >-
  This skill should be used when the user asks to "validate csv data",
  "check json format", or "lint yaml files".
```

| Rule | Constraint |
|------|-----------|
| Length | 1-1024 characters |
| Voice | third person |
| Trigger phrases | at least one quoted phrase |
| Content | trigger conditions only, never workflow |

## Optional fields

### version

Semantic version for the skill. Start at 1.0.0 for new skills.

```yaml
version: 1.0.0
```

Format: `MAJOR.MINOR.PATCH` where:
- MAJOR: breaking changes
- MINOR: new features
- PATCH: fixes and refinements

### allowed-tools

Restrict tools the skill can use. Omit or leave empty to allow all tools.

```yaml
allowed-tools: [Read, Bash, Grep]
```

Common tools by category:

| Category | Tools |
|----------|-------|
| File ops | Read, Write, Edit |
| Search | Glob, Grep |
| Shell | Bash |
| Web | WebFetch, WebSearch |
| Browser | mcp__playwright__* |

### metadata

Extended classification fields used by the Skill Library registry.

```yaml
metadata:
  pack: development
  type: atomic
  design-pattern: tool-wrapper
  skill-type: technical
```

| Field | Required | Values |
|-------|----------|--------|
| pack | yes | meta, retrieval, web, document, development, devops, communication, learning, security, data |
| type | yes | atomic (workflow is for workflow-creator) |
| design-pattern | yes | tool-wrapper, generator, reviewer |
| skill-type | yes | discipline, technical, mindset, reference |

## Claude Code extension fields

Only valid in `agents/claude-code/SKILL.md`. Not for generic SKILL.md.

| Field | Type | Description |
|-------|------|-------------|
| disable-model-invocation | boolean | true = manual `/skill-name` only |
| user-invocable | boolean | false = auto-trigger only, no `/` menu |
| context | string | "fork" = isolated sub-agent |
| agent | string | sub-agent type override |
| model | string | model override |
| argument-hint | string | param hint for `/skill-name` |

## Complete example

```yaml
---
name: data-validator
description: >-
  This skill should be used when the user asks to "validate a csv file",
  "check data format", or "lint json data".
version: 1.0.0
allowed-tools: [Read, Bash, Grep]
metadata:
  pack: data
  type: atomic
  design-pattern: reviewer
  skill-type: technical
---
```
