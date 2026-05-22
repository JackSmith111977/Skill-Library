# Description Writing Guide

Guide to writing effective skill descriptions. Description is the most important field — it determines when the skill triggers.

## Golden rule

**Only describe trigger conditions. Never summarize workflow.**

Right:
```
This skill should be used when the user asks to "create a hook",
"add a PreToolUse hook", or mentions hook events.
```

Wrong (agent may skip body and execute from description alone):
```
This skill creates a hook by reading the config file, registering the
hook function, and writing it to the hooks directory.
```

## Format

Always third person, starting with "This skill should be used when":

```
This skill should be used when the user asks to "trigger phrase 1",
"trigger phrase 2", or mentions "topic".
```

## Trigger phrases

**Requirements**:
- At least one quoted phrase
- 2-5 phrases ideal for good coverage
- Phrases the user would naturally say
- Specific enough to avoid false triggers

Good:
```
"create a csv file from this data", "export to csv", "convert to csv"
```

Too vague:
```
"data"  ← would trigger on every data-related request
"file"  ← would trigger on every file operation
```

## Coverage heuristic

| Trigger phrases | Coverage |
|----------------|----------|
| 0 | failing — no triggers found by CoverageAssessor |
| 1-2 | weak — may miss many activation chances |
| 3-5 | good — covers common phrasings |
| 6+ | ideal — covers edge cases too |

CoverageAssessor in the quality engine scores 0-100 based on trigger count:
- MIN_TRIGGERS = 3 (score penalized below 3)
- IDEAL_TRIGGERS = 6 (full score at 6+)

## Third-person check

Description must:
1. Start with third person ("This skill should be used when...")
2. Use third-person verbs ("creates", "validates", "generates")

ThirdPersonDetector checks both:
- `has_third_person`: description starts with third-person phrasing
- `has_verb_third_person`: body verbs are in third-person form

## Examples

Good description:
```yaml
description: >-
  This skill should be used when the user asks to "validate a csv file",
  "check json schema", "verify yaml format", or "lint xml data".
```

Good description with broader coverage:
```yaml
description: >-
  This skill should be used when the user asks to "create a web search skill",
  "add web research capability", "make a search agent", or mentions
  "web search", "online research", or "internet lookup".
```
