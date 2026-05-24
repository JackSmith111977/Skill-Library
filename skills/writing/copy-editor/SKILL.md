---
name: copy-editor
description: >
  This skill should be used when the user asks to "review this text",
  "copy edit", "proofread", "check grammar", "improve this writing",
  "edit this draft", "polish this text", "clean up this writing",
  "check for errors", or "review this document". Reviews grammar,
  style, clarity, and readability without changing content meaning.
version: 1.0.0
allowed-tools: [Read, Grep]
metadata:
  pack: writing
  design-pattern: reviewer
  skill-type: discipline
  author: Kei
---

# Copy Editor

Review text for grammar, style, clarity, consistency, and readability. Diagnose issues, suggest fixes — does not rewrite content.

## Purpose

Catch writing issues before publication. Focus on correctness and clarity. The author decides which suggestions to apply.

## When to Use

- Draft complete and needs quality pass
- Text has known grammar or style issues
- Consistency check needed (terminology, voice, tense)
- Before publication or submission
- Non-native writing needs fluency polish

## When NOT to Use

- Content needs restructuring or rewriting (use article-writer)
- Research needs validation (use research-assistant)
- Factual accuracy check needed (use research-assistant)
- Text is ultra-short (tweet, status) — review mentally

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| text | yes | Content to review |
| style-guide | no | Specific style rules (APA / Chicago / brand / none) |
| focus | no | Grammar / style / clarity / all (default: all) |
| tone-target | no | Target tone for tone-check pass |
| severity | no | All / major-only (default: all) |

## Steps

### 1. Read Text

Read full text before making any notes. Understand:
- Purpose and audience
- Voice and register
- Argument or narrative flow

### 2. Grammar and Mechanics Check

Systematic pass for:
- Subject-verb agreement
- Tense consistency
- Punctuation (commas, semicolons, dashes)
- Spelling (including US/UK consistency)
- Article and preposition usage
- Sentence fragments and run-ons

### 3. Style and Usage Review

- Jargon and cliché detection
- Passive voice overuse (flag, don't ban)
- Wordiness and redundancy
- Nominalization (e.g. "make a decision" → "decide")
- Vague modifiers (very, really, quite)
- Consistent terminology

### 4. Clarity and Structure

- Paragraph topic sentences present
- Logical flow between paragraphs
- Transitions explicit where needed
- Unclear antecedents (this, that, it)
- Long sentences that could be split

### 5. Consistency Check

- Spelling conventions (US vs UK, one pass)
- Names and terms spelled same way
- Numbers format consistent
- Heading style parallel
- List punctuation parallel

### 6. Report

Organize findings by severity:

**Critical**: Errors that affect meaning or credibility.
**Major**: Style violations, awkward phrasing, consistency.
**Minor**: Preferences, optional improvements.

Per finding: location, issue description, suggestion (not rewrite).

## Validation

- [ ] Every finding has specific location reference
- [ ] Suggestions are diagnostic, not rewrites
- [ ] No content meaning changed
- [ ] Findings categorized by severity
- [ ] Tone assessment included
- [ ] Positive aspects noted (what works well)

## Outputs

- Structured edit report (markdown)
- Categorized by severity: critical / major / minor
- Per finding: location → issue → suggestion
- Overall assessment: ready / minor-revision / major-revision
- Tone and voice consistency note

## Chaining Notes

- **Consumes from**: article-writer, blog-post-writer, academic-writer
- **Used by**: writing-pipeline (step 3, final quality gate)
- **Position**: Always final step in writing pipeline
- **Output format**: `<!-- edit-report -->` marker for downstream tracking
