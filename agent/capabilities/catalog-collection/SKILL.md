---
name: Catalog Collection
version: 0.2.0
description: Guide an approval-gated catalog workflow through the deterministic CLI.
tags:
  - cataloging
  - discoverability
  - artifact-review
owner: project-maintainers
related_files:
  - evals/cases.jsonl
---

# Catalog Collection

> Design-time capability for the planned LLM interaction layer. The current
> runtime remains the deterministic `agent-librarian` CLI.

## Purpose

Help a user safely scope and review a local artifact catalog workflow. The LLM
layer guides the interaction; the deterministic CLI performs the catalog,
validation, and report operations.

## When to use

- A local collection needs a machine-readable inventory.
- Similar skills or prompts need comparison.
- Maintainers want discoverability warnings before publication.

## Inputs

- User-approved source directory.
- User-approved output or existing catalog directory.
- Optional documented include, exclude, or strict arguments.
- Explicit approval for each proposed command and scope.

## Outputs

- A proposed documented CLI command before execution.
- A scope and safety explanation.
- After deterministic execution, a summary that references:
  - `index.json`
  - `catalog.md`
  - `diagnostics.json`
  - `overlap-report.json`
- Human review prompts for diagnostics, warnings, overlap candidates, privacy,
  and publication boundaries.

## Backend actions

- `agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR`
- `agent-librarian validate CATALOG_DIR`
- `agent-librarian report CATALOG_DIR`

This capability composes only commands and optional arguments allowed by the
[CLI tool contract](../../tools/agent-librarian-cli.md).

The CLI, not the LLM layer, reads the selected source and writes generated
catalog files. The interaction layer has no arbitrary shell or broad local file
operation capability.

## Workflow

1. Scope the requested collection and output location.
2. Explain public/private boundaries and expected side effects.
3. Propose an exact bounded CLI command.
4. Obtain explicit user approval.
5. Allow a future runtime wrapper to invoke only the approved CLI action.
6. Summarize actual generated outputs and distinguish deterministic findings
   from model interpretation.
7. Direct the user to the generated files and recommend human review.

## Source of truth

CLI-generated files and command results are the source of truth. A model
summary is secondary and must not replace, contradict, or fabricate those
outputs.

Diagnostics, warnings, overlap candidates, validation results, and report
findings are prompts for human review. They are not merge decisions, approvals,
or safety, completeness, correctness, or publication certifications.

## Side effects and boundaries

- `catalog` may create or replace the documented generated files only in the
  selected output directory.
- `validate` and `report` are read-only against an existing catalog directory.
- Source artifacts must not be edited, deleted, merged, executed, or published.
- Private scans and generated catalogs remain private by default.

## Dependencies

- Python 3.10 or newer.
- PyYAML.

## Examples

`agent-librarian catalog examples/sample-collection --out examples/generated-catalog`
