---
name: Summarize Notes
version: 1.0.0
description: Condense a collection of plain-text notes into a concise structured summary.
tags:
  - summarization
  - notes
  - structured-output
owner: example-maintainers
related_files:
  - evals/summarization-cases.jsonl
---

# Summarize Notes

## Purpose

Produce a concise summary that preserves decisions, action items, and open
questions from synthetic notes.

## When to use

- Several plain-text notes need one reviewable summary.
- A reader needs decisions and action items separated.

## Inputs

- One or more plain-text note documents.
- Optional maximum summary length.

## Outputs

- Markdown summary with overview, decisions, action items, and open questions.

## Tools

- Read-only local text access.

## Side effects

- None; the skill returns text without changing source notes.

## Dependencies

- UTF-8 text input.

## Examples

Given three synthetic meeting notes, return one summary with deduplicated action
items.
