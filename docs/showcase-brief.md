# agent-librarian Showcase Brief

## One-sentence summary

`agent-librarian` is a local, deterministic CLI that catalogs agentic AI
artifacts, validates generated catalog outputs, emits diagnostics, flags
warning conditions, and identifies overlap candidates for human review.

## What this is

`agent-librarian` is a public reference implementation for artifact-first agent
infrastructure. It scans a local collection of Markdown, YAML, and JSON files
and produces an inspectable inventory of artifacts such as agent definitions,
capability modules, prompt templates, tool manifests, schemas, and
protocol-facing manifests.

The project is intentionally small enough to inspect. Its source artifacts,
schemas, generated outputs, diagnostics, tests, CI workflow, and safety
boundaries are all visible in the repository.

## Architecture direction

The showcase is CLI-first: it demonstrates the deterministic backend that
performs `catalog`, `validate`, and `report` actions. A planned LLM
interaction layer can sit in front of this same backend to scope intent,
explain safety boundaries, propose bounded commands, ask for approval before
execution, and summarize the generated outputs.

That interaction layer would orchestrate the workflow, not replace the
cataloging logic or invent findings. CLI-generated files remain the source of
truth for review. This distinction keeps the project precise about what is
implemented today and what is planned for a future agent-facing experience.

## Why it exists

Agentic systems depend on more than prompts. They also depend on artifacts that
describe capabilities, activation conditions, inputs, outputs, tool access,
side effects, dependencies, ownership, safety boundaries, and review status.

Those artifacts need to be addressable, versionable, inspectable, and
governable. `agent-librarian` demonstrates one practical way to inventory and
review them without requiring a hosted service or an autonomous model.

## What it demonstrates

- artifact-first agent system design
- local-only scanning that treats selected files as data
- deterministic generated outputs
- schema-backed catalog validation
- per-file parse diagnostics and strict mode
- warning and overlap surfaces for human review
- configurable scan include and exclude patterns
- explicit public-safety boundaries
- CI-backed validation and release hygiene
- separation between source artifacts and generated review outputs

## How it works at a glance

```text
local artifact collection
  -> safe scanner and structured parsers
  -> artifact classification and metadata normalization
  -> parse diagnostics and review warnings
  -> deterministic overlap scoring
  -> generated catalog and reports
  -> schema validation and human review
```

The scanner does not import, source, evaluate, or execute scanned artifacts.
Normal mode isolates individual parse failures and records them in diagnostics.
Strict mode produces outputs when practical, then exits non-zero when a
selected file failed to parse.

## What it produces

A catalog run writes four files under the selected output directory:

- `index.json`: machine-readable entries and generation metadata
- `catalog.md`: a human-readable inventory with review warnings
- `overlap-report.json`: deterministic overlap candidates
- `diagnostics.json`: per-file parse status, warnings, and sanitized errors

The `validate` command checks the generated JSON against bundled schemas.
Validation confirms expected structure; it does not certify completeness,
semantic correctness, safety, or publication readiness.

## What this is not

It is:

- not a hosted marketplace
- not a private registry
- not an LLM-powered reviewer by default
- not a semantic or vector search system
- not an automatic merge or deduplication engine
- not a safety or correctness certification system
- not a tool that executes scanned artifacts
- not a replacement for human review

The stable CLI and optional runtime wrapper do not use an LLM provider and are
not an LLM-powered autonomous agent. They support a planned two-layer
architecture, not an autonomous agent runtime. Warnings and overlap candidates
are review prompts, not decisions, and a future model summary must not present
them as safety, completeness, approval, or publication-readiness
certifications.

## Why it matters for agentic AI artifacts

The broader Agentic AI Artifact Taxonomy thesis is that reliable agentic
systems need inspectable artifacts around model behavior: schemas,
instructions, capability definitions, tool contracts, outputs, diagnostics,
validation checks, safety boundaries, and release discipline.

The point is not that every agent needs this exact tool. The point is that
agentic systems need inspectable artifacts around them, and those artifacts
need consistent ways to be cataloged, validated, reviewed, and governed.
`agent-librarian` makes that thesis concrete in a small repository.

## Safe demo boundaries

For public demos, use only the public repository, the committed synthetic
sample artifacts, and generated outputs from `examples/sample-collection`.

Do not demo private collections, employer workflows, internal repositories,
private prompts, real traces, memory or state snapshots, credentials, secrets,
regulated or private data, or generated catalogs from non-public sources.

Local and deterministic processing reduces exposure, but it does not make
arbitrary source material safe to publish. Human review of source artifacts
and generated outputs remains required.

## Where to start

1. Read the [project overview](../README.md).
2. Review the [taxonomy-aligned architecture map](taxonomy-architecture-map.md).
3. Follow the [five-minute demo walkthrough](demo-walkthrough.md).
4. Use the [forum demo runbook](forum-demo-runbook.md) for a live presentation
   from a work computer.
5. Read the [public-safe adoption guide](adoption-guide.md) before adapting the
   tool to another collection.
6. Inspect the [synthetic sample collection](../examples/README.md).
7. Review the committed outputs in
   [`examples/generated-catalog`](../examples/generated-catalog/).
8. Read the [architecture](architecture.md),
   [catalog format](catalog-format.md),
   [warnings and overlap](warnings-and-overlap.md), and
   [public-safety guidance](public-safety.md).
