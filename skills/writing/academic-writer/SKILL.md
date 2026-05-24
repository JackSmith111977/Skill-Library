---
name: academic-writer
description: >
  This skill should be used when the user asks to "write an academic
  paper", "draft a research paper", "write a thesis", "compose a
  scholarly article", "write a literature review", "draft a conference
  paper", "write a case study", or "format academic citations".
  Produces structured academic content with proper citations,
  abstract, and methodology section.
version: 1.0.0
allowed-tools: [Read, Write]
metadata:
  pack: writing
  design-pattern: generator
  skill-type: technical
  author: Kei
---

# Academic Writer

Generate structured academic content following scholarly conventions. Proper citations, methodology rigor, formal tone.

## Purpose

Produce academic-quality drafts from research material. Follow citation standards, maintain formal register, structure per academic convention. Draft only — peer review and original research remain author responsibility.

## When to Use

- Academic paper or conference submission needed
- Literature review synthesis required
- Case study write-up from research material
- Thesis chapter draft from notes
- Research proposal draft

## When NOT to Use

- General article needed (use article-writer)
- Blog content needed (use blog-post-writer)
- Text needs review, not generation (use copy-editor)
- Original empirical research — AI cannot conduct this
- Final submission without author verification

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| topic | yes | Paper subject or research question |
| source-material | yes | Research data, notes, or literature |
| paper-type | no | Research paper / review / case-study / proposal / thesis-chapter (default: research-paper) |
| citation-style | no | APA / MLA / Chicago / IEEE / specific-journal (default: APA 7th) |
| target-outlet | no | Journal, conference, or institution |
| sections | no | Custom section order (default: standard IMRaD) |
| word-count-target | no | Approximate target length |

## Steps

### 1. Review Source Material

Read all provided material. Identify:
- Research question or thesis
- Key findings or arguments
- Methodological approach
- Literature landscape
- Gaps in source material

### 2. Draft Abstract and Keywords

Write structured abstract:
- **Background**: 1-2 sentences on context
- **Problem**: Gap or question addressed
- **Method**: Brief approach description
- **Findings**: Key results or arguments
- **Contribution**: What this adds
- **Keywords**: 4-6 terms for indexing

### 3. Draft Body Sections

Follow IMRaD or custom structure:

**Introduction**:
- Broader context → specific problem → research question
- Brief literature situating
- Paper roadmap sentence

**Literature Review** (if applicable):
- Thematic organization
- Critical evaluation, not summary
- Gap identification leading to current work

**Methodology**:
- Approach rationale
- Data/ material description
- Procedure or framework
- Limitations acknowledged

**Results / Findings**:
- Presentation of findings
- Tables or figures where appropriate
- Objective reporting, no interpretation yet

**Discussion**:
- Interpretation of results
- Connection to literature
- Implications
- Limitations

**Conclusion**:
- Summary of contribution
- Future research directions

### 4. Format Citations

Place citations throughout draft:
- Use specified citation style consistently
- Include full reference list at end
- Mark any missing citation data as `[TBD]`

### 5. Academic Tone Polish

- Formal register (no contractions, colloquialisms)
- Passive voice appropriate (method section)
- Hedge claims appropriately (suggests, indicates, may)
- Define acronyms on first use
- Consistent terminology throughout

## Validation

- [ ] Abstract covers all required elements
- [ ] Research question or thesis clearly stated
- [ ] Methodology described in reproducible detail
- [ ] Citations present and consistent style
- [ ] Reference list complete
- [ ] No unsupported claims (each claim has citation or data)
- [ ] Formal academic tone throughout
- [ ] Section structure matches paper-type
- [ ] Word count within target range

## Outputs

- Full paper draft (markdown)
- Abstract and keywords
- Citation list in specified format
- Placeholder notes for author-completed sections (`[NOTE: ...]`)
- Suggested tables or figures (description, not rendered)

## Chaining Notes

- **Consumes from**: research-assistant (literature review input)
- **Feeds into**: copy-editor (for review pass)
- **Standalone path**: Not part of writing-pipeline (academic writing has separate workflow)
- **Author responsibility**: All AI-generated academic content must be verified, cited properly, and checked for plagiarism before submission
