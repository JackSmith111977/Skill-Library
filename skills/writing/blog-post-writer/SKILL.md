---
name: blog-post-writer
description: >
  This skill should be used when the user asks to "write a blog post",
  "draft a blog entry", "create a blog article", "write a blog about",
  "SEO-optimize a post", "write a web article", "draft a newsletter
  post", or "create engaging content for the web". Generates
  SEO-optimized blog content with title, meta description, and
  scannable structure.
version: 1.0.0
allowed-tools: [Read, Write, WebSearch]
metadata:
  pack: writing
  design-pattern: generator
  skill-type: technical
  author: Kei
---

# Blog Post Writer

Generate engaging, SEO-optimized blog content. Structured for web reading — scannable, shareable, action-oriented.

## Purpose

Create blog content that ranks well and engages readers. Balance SEO requirements with genuine readability. Produce drafts ready for platform publishing.

## When to Use

- User asks for blog content specifically
- SEO-optimized web article needed
- Newsletter or content marketing piece
- Thought leadership or opinion post
- List of resources or curated content

## When NOT to Use

- General article needed (use article-writer)
- Academic or formal paper needed (use academic-writer)
- Content needs review, not generation (use copy-editor)
- Short-form social media content

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| topic | yes | Blog post subject |
| target-audience | no | Reader profile (default: general tech audience) |
| tone | no | Casual / professional / provocative (default: casual) |
| seo-keywords | no | Primary and secondary keywords |
| length | no | Short / medium / long (default: medium) |
| format | no | How-to / listicle / opinion / curated / story (default: how-to) |
| call-to-action | no | Desired reader action |

## Steps

### 1. Keyword and Topic Research

If SEO keywords not provided, use WebSearch to identify:
- High-volume terms for topic
- Current trending angles
- Competing content gaps
- Question-based long-tail keywords

Define primary keyword (title target) and 2-3 secondary keywords.

### 2. Outline with SEO Structure

Draft outline optimized for search and scan:
- **Title**: Include primary keyword, under 60 chars, compelling
- **Meta description**: Under 160 chars, include keyword + CTA
- **H1**: Title (one per post)
- **H2 sections**: Include secondary keywords naturally
- **H3 subsections**: Detail and examples
- **Intro**: Hook + problem + what-this-post-solves
- **Conclusion**: Summary + CTA

### 3. Draft Body

Write section by section:
- Opening hook (statistic, question, or bold statement)
- Short paragraphs (2-4 sentences for web scanability)
- Bullet points and numbered lists where appropriate
- Examples, screenshots, or code blocks as needed
- Internal linking opportunities (placeholder)
- Smooth transitions between sections

### 4. SEO Optimization Pass

- Keyword density check (natural, not stuffed)
- Headings contain keywords where natural
- Alt text placeholders for images
- URL slug suggestion
- Readability score (target: grade 8-10 level)
- Featured snippet opportunity (question-answer format)

### 5. Polish Web Formatting

- Add pull-quote-worthy line (for formatting)
- Check scannability: bold key phrases
- Add "TL;DR" or summary block for long posts
- Verify CTA is clear and prominent

## Validation

- [ ] Title ≤ 60 chars, includes primary keyword
- [ ] Meta description ≤ 160 chars
- [ ] H2 sections break up content for scanning
- [ ] Paragraphs ≤ 4 sentences
- [ ] Keyword appears in first 100 words
- [ ] Readability: grade 8-10 level
- [ ] CTA present and specific
- [ ] No keyword stuffing

## Outputs

- Full blog post (markdown)
- Frontmatter with: title, meta-description, slug, tags
- SEO checklist completion
- Suggested featured image prompt (optional)

## Chaining Notes

- **Consumes from**: research-assistant (optional, for data-backed posts)
- **Feeds into**: copy-editor (for review pass)
- **Not used by** writing-pipeline (standalone path; writing-pipeline targets article format)
