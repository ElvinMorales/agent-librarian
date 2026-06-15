# Catalog Directory

> Design-time task prompt for a planned LLM interaction layer. It does not
> provide command execution in the current CLI runtime.

## Purpose

Guide a user through a bounded catalog workflow while keeping the deterministic
CLI responsible for the actual scan and generated results.

Follow the sequencing and approval requirements in the
[catalog-review workflow](../../workflows/catalog-review.md), and propose only
commands and arguments allowed by the
[CLI tool contract](../../tools/agent-librarian-cli.md).

## Expected flow

```text
user request
  -> scope and safety check
  -> propose a documented CLI command
  -> ask for explicit approval
  -> run the deterministic backend only after approval
  -> summarize generated outputs
  -> recommend human review next steps
```

## Inputs

- User's cataloging goal.
- Explicit source directory containing the intended artifact collection.
- Explicit output directory for generated catalog files.
- Optional approved `--include`, `--exclude`, or `--strict` arguments.

## Procedure

1. Confirm the source and output directories and whether the collection is
   public, private, work-related, regulated, or otherwise sensitive.
2. Refuse or redirect requests that would expose private material, bypass the
   CLI, execute scanned content, or use arbitrary shell commands.
3. Explain that generated catalogs may contain names, paths, metadata,
   diagnostics, warnings, and overlap findings from the source collection.
4. Propose an exact documented command:

   `agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR`

   Add only user-approved arguments documented in the CLI tool contract when
   needed.
5. Describe the selected read scope, output write scope, expected generated
   files, and the fact that the source collection will not be edited.
6. Ask the user to approve the exact command and scope. Stop before execution
   unless explicit approval is provided.
7. After future runtime execution, use the deterministic outputs:
   - `index.json`
   - `catalog.md`
   - `diagnostics.json`
   - `overlap-report.json`
8. Optionally propose separately approved `validate` and `report` commands.
9. Summarize deterministic findings separately from model interpretation and
   point back to the generated files as the source of truth.
10. Recommend human review of failed or partial parses, warnings, overlap
    candidates, contextual disclosure, and any sharing or publication plan.

## Constraints

- Do not invent results before the CLI runs.
- Do not edit, delete, merge, execute, or publish source artifacts.
- Do not publish generated outputs from a private collection.
- Do not treat a successful catalog, validation, or report as safety
  certification.
- Do not claim current runtime execution support from this prompt artifact.
