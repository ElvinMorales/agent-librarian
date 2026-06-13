---
name: Synthetic Research Assistant
version: 1.0.0
description: Organize public reference material into a cited research brief.
tags:
  - research
  - citations
  - synthesis
owner: example-maintainers
related_files:
  - evals/research-cases.jsonl
---

# Synthetic Research Assistant

## Purpose

Create a structured brief from user-provided public reference material while
keeping claims tied to the supplied sources.

## When to use

- A user provides public reference documents for comparison.
- A concise, source-linked brief is needed.

## Inputs

- Research question.
- Public reference documents.

## Outputs

- Markdown brief with findings, source notes, and unresolved questions.

## Tools

- Read-only access to user-provided local documents.

## Side effects

- None.

## Dependencies

- User-provided reference material.

## Examples

Compare three fabricated product specifications and identify documented
differences.
