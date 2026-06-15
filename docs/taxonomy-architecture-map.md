# Taxonomy-Aligned Agent Architecture Map

## Purpose

This map shows how `agent-librarian` functions as an inspectable, local
artifact-librarian agent reference implementation. It connects generic
artifact classes from the Agentic AI Artifact Taxonomy to concrete files,
runtime behavior, generated outputs, and review surfaces in this repository.

The files under `agent/` are design-time descriptions of the system's
identity, operating stance, capability, tools, prompts, memory boundary, state
boundary, and governance. The executable CLI is implemented under
`src/agent_librarian/`; it does not load the `agent/` documents as runtime
instructions.

## System summary

`agent-librarian` is a local deterministic CLI that scans selected Markdown,
YAML, and JSON files as data, classifies artifacts, normalizes metadata, emits
diagnostics and warnings, identifies overlap candidates, writes generated
catalog outputs, and validates generated JSON against bundled schemas.

It does not call an LLM or network service, execute scanned artifacts, maintain
a user memory store, or preserve hidden runtime session state. It does not
automatically approve, merge, delete, rewrite, or publish artifacts. Warnings,
overlap candidates, and validation results remain inputs to human review.

## Current and future layers

The current v0.3 repository implements the deterministic CLI backend. Its
commands, parsers, schemas, diagnostics, generated catalogs, and reports are
the current runtime and review artifacts.

A future LLM interaction layer would add user-facing identity and orchestration
artifacts for scoping intent, explaining safety boundaries, proposing bounded
CLI commands, recording approval before execution, and summarizing generated
outputs. It must call the backend through documented command contracts rather
than replace catalog logic, invent findings, or run arbitrary shell commands.
CLI-generated files remain the source of truth; model summaries remain review
aids and cannot certify safety, completeness, approval, or publication
readiness.

For the expanded table that classifies both layers across all 14 taxonomy
buckets, see the
[Two-Layer Artifact Catalog](two-layer-artifact-catalog.md).

## Artifact flow

```text
source artifact collection
  -> deterministic CLI backend
       -> scanner and parsers
       -> classification and normalization
       -> warnings and diagnostics
       -> overlap analysis
       -> generated catalog outputs
       -> schema validation
  -> human review
  -> docs/tests/release iteration
```

The `catalog` command performs the scan-through-output portion of this flow.
The separate, read-only `validate` command checks the generated JSON against
the packaged schemas.

## Taxonomy map

| Taxonomy bucket | Generic artifact class | Possible filenames | Implementation in this repo | Role in `agent-librarian` |
| --- | --- | --- | --- | --- |
| 1. Identity | Agent definition or identity manifest | `agent.yaml`, `AGENTS.md`, package metadata | `agent/agent.yaml`, `agent/persona.md`, `README.md`, `pyproject.toml` | Defines the system's purpose, scope, ownership, package identity, and limits without claiming an autonomous runtime. |
| 2. Operating style | Principles, behavior guidance, or operating constraints | `principles.md`, persona guidance, non-goals | `agent/principles.md`, `agent/persona.md`, `docs/showcase-brief.md`, README non-goals | Establishes framework-neutral, deterministic, conservative, local-only, and human-review-first behavior. |
| 3. Capability modules | Skill or reusable capability bundle | `SKILL.md`, capability package, procedure | `agent/capabilities/catalog-collection/SKILL.md`, `src/agent_librarian/scanner.py`, `parsers.py`, `normalizer.py`, `renderers.py` | Describes and implements the catalog-collection capability from file discovery through normalized output rendering. |
| 4. Tools | Tool manifest, callable command, parser, or permission surface | `tools.yaml`, CLI subcommand, parser module | `agent/tools/tools.yaml`, `src/agent_librarian/cli.py`, the `catalog` and `validate` commands, scanner and parser modules | Provides executable cataloging and validation surfaces with local read scope and writes confined to `--out`. |
| 5. Knowledge and resources | Reference documentation, schemas, examples, or sample data | `README.md`, reference docs, sample collection, schema resources | `docs/`, `examples/sample-collection/`, `examples/README.md`, `src/agent_librarian/schema_data/` | Grounds users, maintainers, tests, and validation in public-safe documentation, fixtures, and packaged contracts. |
| 6. Prompts and interfaces | Prompt template, task instruction, CLI contract, or help text | system prompt, task prompt, CLI usage, example prompt | `agent/prompts/system.md`, `agent/prompts/tasks/catalog-directory.md`, CLI help in `src/agent_librarian/cli.py`, README commands, `examples/sample-collection/prompts/weekly-review.md` | Defines user-facing command contracts and demonstrates that prompts are catalogable artifacts, not instructions executed by the CLI. |
| 7. Memory | Durable remembered knowledge, retention policy, or memory schema | memory policy, memory store, retained facts | `agent/memory/policy.md` and the documented absence of a memory store | Makes explicit that no durable user memory is retained; only explicitly written output files persist. |
| 8. State | Run state, checkpoint, generated snapshot, or execution record | state strategy, `index.json`, diagnostics, checkpoint | `agent/state/state-strategy.md`, `examples/generated-catalog/index.json`, `diagnostics.json`, `overlap-report.json`, `catalog.md` | Defines the stateless command boundary and exposes run results as visible files rather than hidden or resumable session state. |
| 9. Planning and orchestration | Workflow plan, command sequence, router, or handoff process | task procedure, walkthrough, developer workflow, CI job | `agent/prompts/tasks/catalog-directory.md`, `docs/demo-walkthrough.md`, `docs/developer-workflow.md`, `.github/workflows/ci.yml` | Orders scanning, validation, testing, review, deterministic checks, and release handoffs without adding autonomous planning. |
| 10. Guardrails and governance | Safety policy, approval boundary, review rule, or non-goal list | governance policy, safety guidance, warning reference | `agent/governance/policy.md`, `docs/public-safety.md`, `docs/warnings-and-overlap.md`, README safety and non-goals | Defines public/private boundaries, safe defaults, interpretation limits, and decisions that remain with human reviewers. |
| 11. Outputs and schemas | Output contract, generated report, catalog format, or JSON Schema | `*.schema.json`, `index.json`, `catalog.md`, report JSON | `src/agent_librarian/schema_data/*.schema.json`, public `schemas/*.schema.json`, `docs/catalog-format.md`, `examples/generated-catalog/` | Makes catalog entries, diagnostics, overlap findings, and validation contracts inspectable and machine-checkable. |
| 12. Evaluation and observability | Tests, diagnostics, validation checks, CI, or review metrics | test modules, CI workflow, diagnostics report, validator | `tests/`, `.github/workflows/ci.yml`, `examples/generated-catalog/diagnostics.json`, `agent-librarian validate` | Exposes parse outcomes and warning conditions, verifies schemas and deterministic behavior, and catches regressions. |
| 13. Runtime and deployment | Package metadata, entry point, environment, release configuration, or protocol adapter | `pyproject.toml`, CLI entry point, workflow, protocol manifest | `pyproject.toml`, `agent_librarian.cli:main`, `src/agent_librarian/__init__.py`, `.github/workflows/ci.yml`, `examples/sample-collection/mcp/sample-server.json` | Defines supported Python versions, installation, command execution, CI environments, and a synthetic protocol-facing artifact example. |
| 14. Learning and iteration | Changelog, issue backlog, release notes, feedback record, or roadmap | `CHANGELOG.md`, release checklist, issues, milestones | `CHANGELOG.md`, `docs/release-checklist.md`, `docs/developer-workflow.md`, GitHub issues and milestones | Records versioned improvements and reviewable future work; the software itself does not learn from users or alter its behavior automatically. |

## Design-time artifacts

Design-time artifacts define or explain the system before a catalog command
runs:

- `README.md`, `docs/`, and `CHANGELOG.md`
- `agent/` identity, principles, capability, tool, prompt, memory, state, and
  governance documents
- `src/agent_librarian/` source code
- `src/agent_librarian/schema_data/` and public `schemas/`
- `examples/sample-collection/`
- `pyproject.toml` and `.github/workflows/ci.yml`

These artifacts are versioned inputs to implementation, review, packaging, and
release. The synthetic sample collection is also runtime input when used in
the documented demo.

## Runtime outputs

A catalog run writes four explicit artifacts under the selected output
directory:

- `index.json`: normalized machine-readable catalog entries
- `catalog.md`: a human-readable rendering of the catalog
- `diagnostics.json`: per-file parse status, warnings, and sanitized errors
- `overlap-report.json`: deterministic same-type overlap candidates

The committed files in `examples/generated-catalog/` are reproducible outputs
from the synthetic sample collection. The output directory is excluded from
its own source scan when it is inside the input directory.

## Memory and state boundaries

`agent-librarian` does not maintain a user memory store. It does not preserve
hidden conversation state or runtime session state. Generated catalog files
are explicit output artifacts, not hidden memory.

In-memory entries, diagnostics, and overlap candidates exist only for one
process. Generated outputs are not resumable checkpoints and do not cause a
later command to continue a prior run. A later command reads only the paths
and files explicitly supplied to it.

Generated outputs may contain names, paths, metadata, warnings, or review
findings from the scanned collection. They should be reviewed before being
committed or shared. Generated catalogs from private collections do not belong
in this public repository.

## Guardrails and governance surfaces

The repository makes the following boundaries inspectable:

- cataloging is local and makes no network or LLM call
- scanned files are treated as data and are not imported, sourced, evaluated,
  or executed
- safe default excludes omit common source-control, environment, dependency,
  cache, build, and generated-output locations
- repeated `--include` and `--exclude` patterns support deliberate scan scope
- `--strict` exits non-zero when a selected file fails to parse
- `agent-librarian validate` checks generated JSON against bundled schemas
- warning and overlap documentation defines review meanings and limits
- public-safety guidance prohibits private, employer-specific, credential,
  trace, user-data, memory, and runtime-state examples
- humans decide whether findings require correction, consolidation, approval,
  commitment, or publication

These controls reduce accidental exposure and make review conditions visible.
They do not prove that an input collection or generated catalog is safe.

## Evaluation and observability surfaces

The main observable surfaces are:

- `diagnostics.json` parse statuses, warning codes, and sanitized failures
- catalog-entry warnings in `index.json` and `catalog.md`
- deterministic candidates and confidence values in `overlap-report.json`
- bundled JSON Schema validation through `agent-librarian validate`
- unit and integration coverage under `tests/`
- GitHub Actions checks across supported Python versions
- deterministic regeneration with `SOURCE_DATE_EPOCH`

Diagnostics describe extraction outcomes. Warnings and overlap scores identify
conditions for review. Schema validation confirms structure. None of these
surfaces certifies semantic correctness, completeness, safety, or publication
readiness.

## Learning and iteration surfaces

Iteration is explicit and repository-driven rather than learned at runtime:

- issues and milestones define proposed work
- source, docs, schemas, and tests change through reviewed commits
- CI checks the proposed revision
- `CHANGELOG.md` records released behavior
- `docs/release-checklist.md` defines the manual release handoff

The CLI does not train, adapt, retain feedback, or rewrite its own rules after
a run. A future interaction layer must not assume hidden memory or state; any
required approval or run-state artifacts should be explicit and inspectable.

## What this map does not claim

This repository is:

- not a complete agent platform or autonomous agent runtime
- not a hosted marketplace, registry, or network service
- not an LLM-powered reviewer or example of LLM autonomy
- not an automatic governance, approval, merge, deletion, or publishing system
- not a safety, privacy, quality, or correctness certification
- not a replacement for source and generated-output review
- not proof that every cataloged artifact is complete, correct, safe, or ready
  for reuse

The map describes the repository's current inspectable surfaces. It does not
claim that every possible taxonomy artifact must exist in every agentic
system.

## Related docs

- [Project overview](../README.md)
- [Architecture](architecture.md)
- [Taxonomy alignment](taxonomy-alignment.md)
- [Two-Layer Artifact Catalog](two-layer-artifact-catalog.md)
- [Showcase brief](showcase-brief.md)
- [Demo walkthrough](demo-walkthrough.md)
- [Catalog format](catalog-format.md)
- [Warnings and overlap](warnings-and-overlap.md)
- [Public safety](public-safety.md)
- [Developer workflow](developer-workflow.md)
