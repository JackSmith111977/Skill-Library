---
name: research-assistant
description: >
  This skill should be used when the user asks to "research a topic",
  "find information about", "look into", "investigate", "gather data
  on", "search for", "explore the topic of", "do research on", or
  "collect information about" a subject. Also used for cross-source
  fact-checking, verification, and structured research gathering.
version: 1.0.0
allowed-tools: [Read, WebSearch, WebFetch]
metadata:
  pack: writing
  design-pattern: tool-wrapper
  skill-type: technical
  author: Kei
---

# Research Assistant

Cross-source structured research. Collect, verify, and organize information from multiple sources.

## Purpose

Transform broad research questions into structured, verified knowledge. Prioritize source quality over quantity. Produce actionable summary for downstream consumption.

## When to Use

- User asks to research unfamiliar topic
- Need factual grounding before writing
- Cross-source fact-checking required
- Competitive or market intelligence gathering
- Technical or academic literature review

## When NOT to Use

- User already has clear answer — just answer directly
- Real-time data (prices, weather, stocks) — use appropriate API instead
- User wants opinion, not fact — use analysis skill
- Single known source — read it directly

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| topic | yes | Research subject |
| depth | no | Brief / standard / deep (default: standard) |
| sources | no | Preferred sources or types |
| format | no | Summary / structured / compare (default: structured) |
| constraints | no | Time range, language, region filters |

## Steps

### 1. Clarify Topic

Ask user to specify scope if topic is vague. Confirm:
- What aspect most important?
- Any sources to prioritize or avoid?
- Output format preference?

### 2. Search Across Sources

Use WebSearch with multiple query angles:
- Core term search
- Related concept search
- Opposing viewpoint search (when applicable)
- Recent developments filter

Fetch top 3-5 most authoritative results with WebFetch.

### 3. Extract Key Information

Per source, extract:
- Main claims and findings
- Author/source credibility signals
- Publication date and context
- Supporting data or evidence
- Limitations or caveats

### 4. Cross-Validate

Compare claims across sources:
- Consensus points (reported by 2+ independent sources)
- Contradictions (flag with source attribution)
- Unique insights (single source, note as such)
- Outliers or disputed claims

### 5. Structure Output

Format by requested output type:
- **Summary**: 3-5 paragraph synthesis, key takeaways first
- **Structured**: Sections by subtopic, each with findings + sources
- **Compare**: Table by dimension, sources as columns

Every factual claim must have source citation.

## Validation

- [ ] At least 2 independent sources per key claim
- [ ] Source dates within acceptable range
- [ ] Contradictions explicitly flagged, not smoothed
- [ ] No fabricated or hallucinated sources
- [ ] Output includes confidence level per section

## Outputs

- Research brief (markdown, source-cited)
- Source list with credibility assessment
- Open questions or gaps identified
- Suggested next research directions

## Chaining Notes

- **Feeds into**: article-writer, blog-post-writer, academic-writer
- **Used by**: writing-pipeline (step 1), content-research
- **Format**: Output uses `<!-- research-brief -->` marker for downstream parsing
