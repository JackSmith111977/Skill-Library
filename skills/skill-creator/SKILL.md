---
name: skill-creator
description: >-
  This skill should be used when the user asks to "create a skill", "add a new skill",
  "write a skill", "scaffold a skill", "generate a skill", "make a skill",
  or "build a skill".
version: 1.0.0
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
metadata:
  pack: meta
  type: atomic
  design-pattern: generator
  skill-type: technical
---

# skill-creator

Guide user through creating atomic skill that follows Skill Library format. Each step list requirements, then wait for user input.

## Step 1: Clarify requirements

Collect 5 fields before creating anything:

| Field | Required | Allowed values |
|-------|----------|---------------|
| name | yes | kebab-case, 1-64 chars, lowercase letters + hyphens |
| pack | yes | meta / retrieval / web / document / development / devops / communication / learning / security / data |
| design-pattern | yes | tool-wrapper / generator / reviewer |
| skill-type | yes | discipline / technical / mindset / reference |
| description | yes | brief one-liner describing what skill does |

Questions to ask user:

- "What should the skill do?" — derive name + description from answer
- "Which pack does it belong to?" — if unsure, suggest based on functionality
- "What design pattern fits?" — tool-wrapper (domain knowledge), generator (template output), reviewer (checklist)
- "What skill type?" — discipline (rules), technical (methods), mindset (thinking models), reference (docs)

Only atomic skills (not workflows). For workflow skills use workflow-creator.

**Allowed design patterns for atomic skills**: tool-wrapper, generator, reviewer. Inversion and pipeline are workflow-only.

## Step 2: Create directory

Path: `skills/<pack>/<name>/`

```
skills/<pack>/<name>/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

Create all 4 entries. References/scripts/assets can be empty directories (add `.gitkeep` if needed).

## Step 3: Write SKILL.md frontmatter

```yaml
---
name: <skill-name>           # kebab-case, matches directory name
description: >               # third person, trigger phrases in quotes
  This skill should be used when...
version: 1.0.0               # semver, start at 1.0.0
allowed-tools: [Read, Bash]  # tools the skill needs
---
```

**name rules**:
- 1-64 characters
- Lowercase letters, digits, hyphens only
- Must not start or end with hyphen
- No consecutive hyphens
- Must match directory name

**allowed-tools rules**:
- List only tools the skill actually needs
- Common tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch
- Format as YAML list: `[Read, Bash, Grep]`

## Step 4: Write description

**Hard requirements**:
- 1-1024 characters
- Third person: "This skill should be used when..."
- Contains trigger phrases in quotes, e.g. `"create a skill"`, `"add a new skill"`
- Multiple trigger phrases improve discovery
- **Only describe trigger conditions, never summarize workflow**

Good:
```yaml
description: >-
  This skill should be used when the user asks to "validate data", "check file format",
  "verify csv", or "lint json".
```

Bad (summarizes workflow):
```yaml
description: >-
  This skill reads a file, checks its schema, validates each row, and reports errors.
```

See `references/description-guide.md` for detailed guide with examples.

## Step 5: Write body

**Format rules**:
- Markdown with clear section hierarchy
- Imperative mood or infinitive (verb-first), no second person
- Recommended 1500-2000 words, hard limit 5000 words / 500 lines

**Structure template**:

```markdown
# skill-name

Brief one-liner on what this skill does.

## Workflow

Step-by-step process for the agent to follow.

## Rules

Specific rules the agent must follow.

## Examples

1-3 examples showing usage.
```

**Keep body lean**: detailed reference content goes in `references/`. If body approaches 300 lines, start splitting.

See `references/frontmatter-reference.md` for all allowed metadata fields.
See `references/quality-standards.md` for lint thresholds.

## Step 6: Verify

Run lint to confirm format compliance:

```bash
cd <project-root>
skill-manager lint skills/<pack>/<name>
```

**Must pass** (score = 100, no errors). If lint fails, fix issues and re-run.

Check trigger phrases in description — run at least 3 mental tests:
1. Would a user naturally say one of these phrases?
2. Is each phrase specific enough to avoid false triggers?
3. Are the most likely trigger phrases included?
