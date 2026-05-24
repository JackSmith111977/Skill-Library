---
name: article-writer
description: >
  This skill should be used when the user asks to "write an article",
  "draft an article", "create a article about", "turn these notes into
  an article", "write a piece on", "compose an article", or "structure
  this content into an article". Converts outlines or notes into
  well-structured prose with sections and transitions.
version: 1.0.0
allowed-tools: [Read, Write]
metadata:
  pack: writing
  design-pattern: generator
  skill-type: technical
  author: Kei
---

# Article Writer

Convert outlines, notes, or research into structured articles with clear narrative flow.

## Purpose

Transform raw material (notes, outline, research brief) into publication-ready article. Maintain consistent voice, logical section progression, and reader-appropriate depth.

## When to Use

- User has outline or notes and wants full draft
- Research brief exists and needs article conversion
- User describes topic and wants structured long-form piece
- Content needs reorganization into article format

## When NOT to Use

- Output needed is blog post (use blog-post-writer)
- Output needed is academic paper (use academic-writer)
- Content needs review, not generation (use copy-editor)
- User just needs short paragraph or direct answer

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| topic | yes | Article subject |
| source-material | yes | Outline, notes, or research brief |
| tone | no | Professional / conversational / neutral (default: professional) |
| audience | no | General / technical / executive (default: general) |
| length | no | Short / medium / long (default: medium) |
| format | no | Standard / listicle / how-to / opinion (default: standard) |

## Steps

### 1. Review Source Material

Read all input material. Identify:
- Core thesis or main message
- Key supporting points
- Gaps requiring additional content
- Natural section breaks

If source is research brief (`<!-- research-brief -->` marker), extract structured findings directly.

### 2. Draft Section Outline

Create section map:
- Hook / introduction context
- 3-5 body sections with clear headings
- Logical progression (chronological, problem-solution, general-to-specific)
- Conclusion with takeaways

Each section: 1 sentence summary + key points to cover.

### 3. Write Body Sections

Per section:
- Opening transition sentence (connects from previous)
- Core content with examples or evidence
- Closing sentence (sets up next section)
- Inline citations if source material includes references

### 4. Write Introduction and Conclusion

**Introduction**: Hook → context → thesis → roadmap.
**Conclusion**: Summary → key takeaway → call-to-action or forward look.

### 5. Polish and Format

- Consistent heading hierarchy (ATX-style `##` / `###`)
- Paragraphs: 3-5 sentences, one idea each
- Transition check: each section flows naturally
- Remove redundancy and filler

## Validation

- [ ] Clear thesis statement in first 2 paragraphs
- [ ] Each section supports thesis
- [ ] Transitions between all sections
- [ ] No orphan sections (every section connected)
- [ ] Consistent tone throughout
- [ ] Article length matches requested length
- [ ] Readable at target audience level

## Outputs

- Single markdown file
- Section headings (## level)
- Optional: suggested title (frontmatter `title:`)
- Optional: excerpt (first paragraph suitable as preview)

## Chaining Notes

- **Consumes from**: research-assistant (`<!-- research-brief -->` format)
- **Feeds into**: copy-editor (for review pass)
- **Used by**: writing-pipeline (step 2)
