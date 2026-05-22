# Quality Standards Reference

Lint rules and quality thresholds for the Skill Library project.

## Atomic skill lint rules (7 checks)

| # | Rule | Threshold | Level |
|---|------|-----------|-------|
| 1 | name format | 1-64 chars, lowercase+hyphens, matches dir | ERROR |
| 2 | description length | 1-1024 chars | ERROR |
| 3 | description triggers | has quoted trigger phrases + third person | WARNING |
| 4 | body length | ≤ 500 lines, ≤ 5000 words | WARNING |
| 5 | file references | all referenced files must exist | ERROR |
| 6 | allowed-tools format | valid YAML list of tool names | ERROR |
| 7 | metadata format | valid key-value, version semver | WARNING |

## Bloat thresholds

| Metric | Limit | Action |
|--------|-------|--------|
| Body lines | 500 max | split into references/ |
| Body words | 5000 max | split into references/ |
| Reference files | 10 max | merge related references |

## Description quality scoring

| Score | Grade | Meaning |
|-------|-------|---------|
| 100 | perfect | 6+ triggers, third person, good verbs |
| 80-99 | good | 3+ triggers, third person |
| 60-79 | fair | meets minimum triggers |
| <60 | poor | missing triggers or third person |

Scored by CoverageAssessor:
- MIN_TRIGGERS = 3 (bare minimum)
- IDEAL_TRIGGERS = 6 (full score)

## Lint result format

```
score: 0-100 (starts at 100, decremented per finding)
passed: true/false (true only if score >= 100)
errors: list of rule violations (fatal)
warnings: list of rule violations (non-fatal)
```

## Common lint failures and fixes

| Failure | Likely cause | Fix |
|---------|-------------|-----|
| name format error | uppercase or consecutive hyphens | use kebab-case |
| description too short | less than 1 char | write description in third person |
| no trigger phrases | description missing quoted text | add "trigger phrases" in quotes |
| file reference broken | SKILL.md links to nonexistent file | create file or remove link |
| body too long | > 500 lines / > 5000 words | move content to references/ |
