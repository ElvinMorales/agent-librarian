# Public Safety

This repository demonstrates cataloging with synthetic design-time artifacts.
It is not a suitable place for private operational collections.

## Do Not Commit

- credentials, access material, or private certificates
- private service addresses or workspace locations
- employer-, client-, or user-specific workflows
- regulated or personal data
- real messages, retained memory, run checkpoints, logs, or traces
- production tool results or unsanitized generated outputs

## Prefer

- generic descriptions and fabricated identifiers
- schemas, templates, and policies instead of runtime records
- synthetic examples with explicit labels
- documented permissions, side effects, and review boundaries
- framework-neutral artifact classes with protocol mappings at the edge

## Scanner Boundaries

The CLI does not execute files or call external services. That reduces risk but
does not make arbitrary input safe to publish. Warning patterns are only a
rough review aid and cannot prove that a collection is sanitized.

Before publishing generated catalogs, review both source artifacts and
generated outputs for contextual disclosure.

See the [public-safe adoption guide](adoption-guide.md) for a step-by-step
workflow using synthetic examples and private placeholder paths.

## Presentation Output Boundaries

The default `present` command is deterministic, offline, provider-free, and
requires no API key. Its `overview.html` still inherits the source catalog's
sensitivity because it can expose artifact names, paths, diagnostics, warnings,
and overlap information.

The explicit `present --narrate` path is online and Anthropic-backed. It sends
only generated `index.json`, `diagnostics.json`, and `overlap-report.json`
facts, but those facts can still be sensitive. Use narration only when sending
that metadata to the configured provider is acceptable. The generated
`narrative.md` may repeat sensitive names, paths, warnings, and overlap
information.

Do not commit or publicly share `overview.html`, `narrative.md`, or
`narrative-provenance.json` created from private catalogs. Public demos must use
synthetic catalog data. Model narrative is a secondary review aid; it does not
certify safety, privacy, correctness, completeness, compliance, approval, or
publication readiness. Deterministic catalog facts remain the source of truth.

## LLM Interaction Boundary

Any LLM interaction layer, including optional presentation narration, must
preserve these public/private boundaries.

It must not:

- run arbitrary shell commands or bypass the deterministic CLI
- publish or expose private scans or generated catalogs
- certify artifacts as safe, complete, approved, or ready to publish
- imply employer sponsorship, approval, or endorsement
- assume hidden memory or state that changes scope or approval boundaries

CLI-generated files remain explicit review artifacts and the source of truth.
Model summaries do not replace human review.

For the planned LLM interaction layer's detailed refusal and redirect
patterns, see the
[LLM-Layer Public Safety Policy](../agent/policies/public-safety.md).
