---
name: Summarize Documents
version: 1.0.0
description: Condense a collection of plain-text documents into a concise structured summary.
tags:
  - summarization
  - documents
  - structured-output
owner: example-maintainers
related_files:
  - evals/summarization-cases.jsonl
---

# Summarize Documents

## Purpose

Produce a concise summary that preserves decisions, action items, and open
questions from synthetic documents.

## When to use

- Several plain-text documents need one reviewable summary.
- A reader needs decisions and action items separated.

## Inputs

- One or more plain-text documents.
- Optional maximum summary length.

## Outputs

- Markdown summary with overview, decisions, action items, and open questions.

## Tools

- Read-only local text access.

## Side effects

- None; the skill returns text without changing source documents.

## Dependencies

- UTF-8 text input.

## Examples

Given three synthetic project documents, return one summary with deduplicated
action items.
