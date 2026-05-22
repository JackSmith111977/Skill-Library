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

Manages the Skill Library: lint, register, mount, unmount, and query skills. This meta-skill guides the AI to perform management operations directly via file operations and Python module calls.

## Prerequisites

- Skill Library directory with `state.json` and `skills/` directory
- Python dependencies installed: `pip install -r requirements.txt`
- Target agent skill directories exist (e.g. `~/.claude/skills/` for Claude Code)

## Management Operations

All operations follow: **read state → precondition check → execute → write state**.

### Lint — quality check

Run quality checks on a skill directory via Python engine:

```bash
# Atomic skill
python -m skill_library.quality.lint <skill-path>

# Workflow skill (extra 4 rules)
python -m skill_library.quality.lint <skill-path> --workflow

# With profile
python -m skill_library.quality.lint <skill-path> --profile claude-code
```

**Validates:** name format, description (profile-aware), body length, reference files exist, allowed-tools format, metadata, bloat. Workflow: ref resolution, step completeness, gate markers, dep cycles.

### Mount — install skill to agent

Mount copies a skill directory to target agent's skill directory and updates state.

```
Step 1: Verify skill is registered and quality-status == "passed"
  Read state.json → skills["<name>"]["quality-status"]
  If not "passed", run lint first.

Step 2: Copy skill directory to agent path
  cp -r <skill-dir> <agent-path>/<name>/
  Example: cp -r skills/dev/my-skill ~/.claude/skills/my-skill

Step 3: Update state.json
  state["agents"]["<agent-id>"]["skills"]["<name>"] = {
    "status": "mounted",
    "version": "<version>",
    "adapter": "generic"
  }
  state["skills"]["<name>"]["mount-status"] = "mounted"
  state["skills"]["<name>"]["mounted-to"].append("<agent-id>")
```

**Precondition:** skill exists, quality-status == "passed", agent registered.

### Unmount — remove skill from agent

Unmount removes skill directory from agent and updates state.

```
Step 1: Verify skill is mounted to target agent
  Read state.json → check agents["<agent-id>"]["skills"]["<name>"]

Step 2: Remove skill directory from agent path
  rm -rf <agent-path>/<name>/
  Example: rm -rf ~/.claude/skills/my-skill

Step 3: Update state.json
  del state["agents"]["<agent-id>"]["skills"]["<name>"]
  state["skills"]["<name>"]["mount-status"] = "unmounted"
  state["skills"]["<name>"]["mounted-to"].remove("<agent-id>")
```

**Precondition:** skill mounted to agent.

### Register — add skill to state

Register scans a skill directory, reads SKILL.md frontmatter, and writes to state.json.

```python
# Via Python directly
python -c "
from skill_library.registry.scanner import scan_skills
from skill_library.registry.parser import parse_skill_md
from skill_library.state.manager import StateManager

sm = StateManager('state.json')
state = sm.load()
skills = scan_skills('<skills-dir>')
for s in skills:
    meta = parse_skill_md(s)
    name = meta['name']
    state.setdefault('skills', {})[name] = {
        'name': name,
        'path': str(s),
        'version': meta.get('version', '0.0.0'),
        'mount-status': 'unmounted',
        'quality-status': 'unchecked',
    }
sm.save(state)
"
```

### Status — query state

Read state.json to inspect registered skills, mounted status, agent assignments.

```python
python -c "
from skill_library.state.manager import StateManager
sm = StateManager('state.json')
state = sm.load()
# Show all skills
for name, info in state.get('skills', {}).items():
    print(f'{name}: mount={info[\"mount-status\"]} quality={info[\"quality-status\"]}')
# Show agents
for aid, info in state.get('agents', {}).items():
    print(f'Agent {aid}: {info[\"path\"]} skills={list(info.get(\"skills\", {}).keys())}')
"
```

## Multi-Agent Mounting

Same skill can mount to multiple agents. Each agent has own skill directory.

```
Mount to Agent A:  cp -r skills/pack/skill  agent-A-path/skill
Mount to Agent B:  cp -r skills/pack/skill  agent-B-path/skill
Unmount from A:    rm -rf agent-A-path/skill  (B unaffected)
```

state.json tracks per-agent via `agents[agent-id].skills[name]` and global `skills[name].mounted-to[]`.

## State Management

Two state machines:

```
mount-status:  unmounted → mounted ↔ outdated
quality-status: unchecked → passed ↔ failed
```

Mount requires quality-status == "passed". When skill updates (SKILL.md changes), mount-status becomes "outdated" — remount to refresh.

## Classification

Each skill has optional classification:

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
2. Frontmatter is valid YAML (via yaml.safe_load)
3. name: 1-64 chars, lowercase+hyphens, matches dir name
4. description: 1-1024 chars, profile-aware trigger check
5. version: valid semver (defaults to 0.0.0)
6. Body length ≤ 500 lines
7. allowed-tools format (skill-library profile only)

Workflow skills (4 additional):
8. All @skill-name references resolve to existing directories
9. Step numbering starts at 1 and is continuous
10. Step dependency graph has no cycles
11. Inversion pattern contains STAGE_GATE markers

## Batch Operations

```bash
# Lint all project skills
for dir in skills/*/; do
  python -m skill_library.quality.lint "$dir"
done

# Lint a specific pack
python -m skill_library.quality.lint skills/dev

# Register all skills in a directory
python -c "
from skill_library.registry.scanner import scan_skills
from skill_library.registry.parser import parse_skill_md
from skill_library.state.manager import StateManager
sm = StateManager('state.json')
state = sm.load()
for s in scan_skills('skills'):
    meta = parse_skill_md(s)
    name = meta['name']
    state.setdefault('skills', {})[name] = {'name': name, 'path': str(s), 'mount-status': 'unmounted', 'quality-status': 'unchecked'}
sm.save(state)
"
```

