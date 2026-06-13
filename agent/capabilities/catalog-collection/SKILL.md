---
name: Catalog Collection
version: 0.1.0
description: Scan a local artifact directory and create reviewable catalog outputs.
tags:
  - cataloging
  - discoverability
  - artifact-review
owner: project-maintainers
related_files:
  - evals/cases.jsonl
---

# Catalog Collection

## Purpose

Create a normalized inventory of supported agentic AI artifact files and flag
metadata gaps or likely overlap for human review.

## When to use

- A local collection needs a machine-readable inventory.
- Similar skills or prompts need comparison.
- Maintainers want discoverability warnings before publication.

## Inputs

- Path to a local directory.
- Path to an output directory.

## Outputs

- JSON catalog index.
- Markdown catalog.
- JSON overlap report.

## Tools

- Local read-only file scanning.
- Local writes confined to the selected output directory.

## Side effects

- Creates or replaces the three documented generated output files.

## Dependencies

- Python 3.10 or newer.
- PyYAML.

## Examples

`agent-librarian catalog examples/sample-collection --out examples/generated-catalog`
