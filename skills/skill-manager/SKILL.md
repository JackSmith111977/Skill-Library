---
name: skill-manager
description: >
  This skill should be used when the user asks to "manage skills",
  "create a new skill", "lint a skill", "mount" or "unmount" a skill,
  "register" a skill, "list" or "query" skills, or manage the Skill
  Library. Also used when the user wants to check skill quality,
  classify a skill, or view the skill registry.
version: 1.0.0
allowed-tools: [Bash, Read, Write, Glob, Grep]
argument-hint:
---

# Skill Manager

Manages the Skill Library: create, lint, register, mount, unmount, and query skills.

## Quick Start

```bash
# Lint a skill
skill-manager lint ./skills/my-skill

# Create a new skill
skill-manager create my-skill --pack dev --type atomic --design-pattern pipeline

# Register newly created skills
skill-manager register ./skills/my-skill

# List registered skills
skill-manager list

# Mount a skill
skill-manager mount my-skill

# Unmount a skill
skill-manager unmount my-skill

# Load a skill into context
skill-manager load my-skill --level L2
```

## CLI Commands

### `skill-manager lint <skill-path>`

Runs quality checks on a skill directory. Returns exit code 0 (pass) or 1 (fail).

**Options:**
- `--json` — output JSON report

**Validates:**
- Atomic skills: SKILL.md exists, frontmatter complete, name/description/version valid, body length limits, type+design-pattern declared, path matches name
- Workflow skills (additional): dependency refs resolve, step numbering continuous, dep graph acyclic, gate markers present for Inversion pattern

### `skill-manager create <skill-name>`

Creates a new skill directory with SKILL.md from a template.

**Options:**
- `--pack <pack>` — skill pack (default: "default")
- `--type <type>` — type: atomic|workflow|hybrid
- `--design-pattern <pattern>` — pattern: pipeline|inversion|agentic-rag|chain|parallel
- `--dir <dir>` — output directory (default: current dir)

**Templates:**
- `atomic`: single-purpose skill with standalone instructions
- `pipeline`: sequential steps, each building on previous output
- `inversion`: user-driven flow with STAGE_GATE halts for confirmation

### `skill-manager register <skill-path>`

Registers a skill in the registry. The registry tracks name, path, version, type, design-pattern, pack, category, mount-status, and quality-status.

**Options:**
- `--category <cat>` — category tag
- `--force` — re-register even if already registered

### `skill-manager list`

Lists all registered skills. Shows name, type, pack, mount-status, quality-status.

**Options:**
- `--type <type>` — filter by type
- `--pack <pack>` — filter by pack
- `--design-pattern <pattern>` — filter by pattern
- `--status <status>` — filter by mount-status
- `--json` — JSON output

### `skill-manager mount <skill-name>`

Mounts a skill (requires quality-status == "passed"). Mounted skills are available for use.

### `skill-manager unmount <skill-name>`

Unmounts a mounted skill.

### `skill-manager load <skill-name>`

Loads a skill into context at the specified level. Used during runtime.

**Options:**
- `--level L1|L2|L3` — load level (default: L1)
- `--path <path>` — skill path (default: from registry)

**Load Levels:**
- `L1` — metadata only (name + description), ~100 tokens
- `L2` — full SKILL.md body, ~500-2000 tokens
- `L3` — body + bundled resources (references/, assets/), unlimited

### `skill-manager --version`

Shows version.

## State Management

The system uses two state machines:

```
mount-status: unmounted → mounted ↔ outdated
quality-status: unchecked → passed ↔ failed
```

Mount requires quality-status == "passed". When a skill is updated (SKILL.md changes), mount-status becomes "outdated" — remount to refresh.

## Classification

Each skill has a two-dimensional classification:

- **design-pattern**: pipeline | inversion | agentic-rag | chain | parallel
- **skill-type**: atomic | workflow | hybrid

## Directory Layout

Skills live under `skills/<pack-name>/<skill-name>/`. Each skill has:

- `SKILL.md` — required: frontmatter + body
- `references/` — optional: reference docs, loaded at L3
- `scripts/` — optional: executable scripts
- `assets/` — optional: templates, resources

## Quality Rules

Atomic skills (7 checks):
1. SKILL.md exists
2. Frontmatter is valid YAML
3. name field present and non-empty
4. description field present and non-empty
5. version is valid semver (defaults to 0.0.0)
6. Body length ≤ 500 lines
7. Skill directory name matches name field

Workflow skills (4 additional):
8. All @skill-name references resolve to existing directories
9. Step N numbering starts at 1 and is continuous
10. Step dependency graph has no cycles
11. Inversion pattern SKILL.md contains STAGE_GATE markers

## Quality Commands

```bash
# Lint all skills
for dir in skills/*/; do
  skill-manager lint "$dir"
done

# Lint a specific pack
skill-manager lint skills/dev
```
