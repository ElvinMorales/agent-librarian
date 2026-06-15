# Agent Interaction Schemas

## Purpose

These design-time schemas define model-authored output contracts for the
planned LLM interaction layer.

## Current status

The current deterministic `agent-librarian` CLI does not load or enforce these
schemas. Runtime wrappers, provider integration, and command execution adapters
remain separately scoped future work.

## Included schemas

- [`review-summary.schema.json`](review-summary.schema.json): contract for an
  evidence-bounded model-authored review summary.
- [`review-summary.example.json`](review-summary.example.json): synthetic
  example grounded only in `examples/generated-catalog`.

## Source-of-truth boundary

CLI-generated files and command outputs remain the source of truth. A model
summary is a secondary review aid and must not invent or override deterministic
evidence.

Schema validation and model summaries do not certify safety, privacy,
correctness, completeness, approval, or publication readiness. Warnings and
overlap candidates remain review prompts. Humans decide correction,
consolidation, deletion, sharing, and publication, and private outputs remain
private.

## Related artifacts

- [CLI tool contract](../tools/agent-librarian-cli.md)
- [Catalog-review workflow](../workflows/catalog-review.md)
- [LLM-layer public-safety policy](../policies/public-safety.md)
- [Runtime state and approval logs](../runtime/state-and-approval-log.md)
- [Safe-scan eval cases](../evals/safe-scan-cases.md)
- [Two-Layer Artifact Catalog](../../docs/two-layer-artifact-catalog.md)
