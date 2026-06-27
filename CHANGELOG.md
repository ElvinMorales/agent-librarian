# Changelog

All notable changes to this project are documented here.

## Unreleased

No changes yet.

## 0.6.0 - 2026-06-27

v0.6.0 — Presentation Layer

This release adds a human-readable presentation layer for generated artifact
catalogs while keeping the default CLI offline and deterministic.

### Added

- Added the offline `present` command, which renders a self-contained,
  deterministic `overview.html` from existing generated catalog facts.
- Added explicit optional `present --narrate` support, with the Anthropic SDK
  available only through the `narrate` extra.
- Added `narrative.md` and `narrative-provenance.json` for narrated runs.
- Added provenance containing a digest over the exact generated JSON payload
  sent to the model.
- Added a synthetic offline presentation demo, a static synthetic narrated
  presentation demo, and a presentation demo walkthrough.
- Added safety documentation clarifying sensitivity inheritance and requiring
  synthetic data for public presentation demos.

### Changed

- Documented the presentation workflow and review surfaces while preserving
  deterministic generated facts as the source of truth.

### Safety / Boundaries

- The default `present` path is offline, deterministic, provider-free, and
  requires no API key; narration is an explicit online opt-in.
- Presentation outputs inherit source sensitivity, and public demos must use
  synthetic data.
- Model narrative is a secondary review aid, not certification of safety,
  privacy, correctness, completeness, compliance, approval, or publication
  readiness.

### Validation

- Added presenter and narration coverage, committed synthetic demo checks,
  package conformance validation, and full CLI and pytest release validation.

## 0.5.0 - 2026-06-16

v0.5.0 — Portable LLM Agent Packages

### Added

- Added portable LLM agent package architecture.
- Added canonical framework-neutral Agent Librarian identity artifact.
- Added shared package manifest schema/example and conformance docs.
- Added Claude package for Claude Code, Claude Enterprise adaptation, and
  cowork demos.
- Added OpenAI package adapters for Codex, GPT, and ChatGPT Projects.
- Added cross-platform demo guides.
- Added package conformance checker and pytest coverage.

### Notes

- The deterministic CLI remains the source of truth.
- Claude Code and Codex packages are local-command-capable only through
  documented approval-gated workflows.
- GPT and ChatGPT Project packages are advisory-only unless a future
  Action/API wrapper is implemented.
- No provider integration, network behavior, MCP server, or autonomous
  execution is included.

## [0.4.0] - 2026-06-15

### Added

- Added a two-layer architecture model for a planned LLM interaction layer,
  with the deterministic CLI backend remaining the source of truth.
- Added agent-layer design artifacts covering identity, operating boundaries,
  prompts, capabilities, governance, memory, state, tools, policies, evals,
  runtime state, and schemas.
- Added a documented CLI tool contract and an approval-gated catalog-review
  workflow for scoped proposals, exact approval, deterministic execution,
  validation, reporting, and human-review handoff.
- Added an LLM-layer public-safety policy and safe-scan eval cases.
- Added runtime state and approval-log artifact designs.
- Added a review-summary JSON Schema and synthetic example.
- Added an optional local runtime wrapper prototype for proposing and
  exact-approval execution of documented `catalog`, `validate`, and `report`
  actions.
- Added runtime-wrapper tests for proposals, approval, execution, sensitivity,
  records, and safety boundaries.

### Changed

- Updated roadmap, taxonomy architecture, and README references for the v0.4
  LLM-layer and runtime-prototype artifact set.
- Clarified that the stable CLI remains deterministic and that the optional
  runtime wrapper does not call an LLM provider, use network access, or expose
  arbitrary shell execution.

### Safety

- The runtime wrapper supports only documented `catalog`, `validate`, and
  `report` actions and requires exact command approval before execution.
- `unclear` and `work-internal` execution are blocked by the prototype.
- Runtime records are written only when explicitly requested, and generated
  outputs and records inherit source sensitivity.
- Validation, reports, and review summaries remain review aids, not safety,
  correctness, completeness, approval, or publication certification.

### Not included

- No LLM provider integration, network calls, or arbitrary shell execution.
- No autonomous publication, approval, deletion, merge, or source-editing
  behavior.
- No PyPI publishing or release artifact upload in this repository change.

## [0.3.0] - 2026-06-14

### Added

- Added an AI expert forum showcase brief that frames `agent-librarian` as
  deterministic, artifact-first infrastructure.
- Added a five-minute demo walkthrough using the synthetic sample collection.
- Added a taxonomy-aligned architecture map covering all 14 agentic AI
  artifact buckets.
- Added warning-reference synchronization checks backed by centralized
  warning-code definitions.
- Added a read-only `agent-librarian report` command for summarizing generated
  catalog review surfaces.
- Added a public-safe adoption guide for adapting the tool to local
  collections without publishing private material.

### Changed

- Strengthened project documentation around design-time artifacts, runtime
  outputs, memory/state boundaries, governance, observability, and human
  review.
- Centralized warning-code definitions for catalog, diagnostics, overlap, and
  partial-status behavior.

### Safety and non-goals

- The report command does not rescan source files, call an LLM or network
  service, mutate generated outputs, or make artifact-management decisions.
- Public demos and examples remain limited to synthetic repository fixtures.
- Generated catalogs from private collections remain private unless
  explicitly reviewed and sanitized.
- PyPI/package registry publishing remains out of scope.
- Schema versions remain unchanged.

## [0.2.0] - 2026-06-14

v0.2.0 focuses on trust and diagnostics: making local artifact catalogs easier
to inspect, validate, test, and review.

### Added

- Per-file parse diagnostics with `parsed`, `partial`, `skipped`, and `failed`
  statuses, sanitized errors, and deterministic warning codes in
  `diagnostics.json`.
- `--strict` catalog mode, which writes outputs when practical and exits
  non-zero when any selected file fails to parse.
- `agent-librarian validate` for checking generated catalog JSON against
  packaged schema resources without network access.
- Repeated `--include` globs and repeated or comma-separated `--exclude`
  patterns for narrowing scans while preserving the safe default excludes.

### Changed

- The selected output directory is excluded when it is under the source root,
  and excluded files do not enter catalog entries or diagnostics.
- GitHub Actions CI runs the CLI, catalog regeneration, schema validation,
  tests, and whitespace checks on Python 3.10, 3.11, and 3.12.
- CI fixes `SOURCE_DATE_EPOCH` and verifies that committed synthetic generated
  outputs remain deterministic and current.
- Local test guidance includes Windows-friendly pytest temporary-directory
  handling without changing the default test command.

### Documentation

- Added contributor workflow guidance for setup, validation, branch hygiene,
  deterministic outputs, Codex handoffs, and public-safe changes.
- Documented warning codes, diagnostics interpretation, overlap scoring
  thresholds, suggested human review, and the limits of automated findings.

### Safety and boundaries

- Scanning remains local and deterministic. Selected artifacts are inspected
  as data and are never imported, sourced, evaluated, or executed.
- Warnings and overlap candidates are review aids, not safety, correctness, or
  publication-readiness certifications.
- Schema validation checks generated JSON structure; it does not certify
  completeness, semantic correctness, safety, or absence of private data.
- Committed examples and generated catalogs remain synthetic and public-safe.

### Non-goals for v0.2.0

- No hosted marketplace.
- No automatic merge or deduplication.
- No LLM-powered review by default.
- No private registry support.
- No semantic search or vector indexing.
- No execution of scanned artifacts.
- No certification that catalogs are safe, complete, or publication-ready.

### v0.3.0 roadmap candidates

These are candidates for future work, not commitments or scheduled features:

- Warning-reference synchronization checks.
- Richer scan configuration, such as a config file or ignore file.
- Better catalog diffing across runs.
- Richer templates and synthetic examples for common artifact types.
- Broader schema validation coverage.
- Optional export formats.
- Improved public-safety review helpers.
- Release tagging and package distribution hygiene.

## [0.1.0] - 2026-06-13

### Added

- Local-only `agent-librarian catalog` CLI.
- Safe Markdown, YAML, and JSON scanning and metadata extraction.
- Framework-neutral artifact classification aligned to 14 taxonomy buckets.
- Discoverability and public-safety review warnings.
- Deterministic overlap candidate reporting with no automatic merges.
- JSON and Markdown catalog renderers and JSON Schemas.
- Synthetic sample collection, generated outputs, evaluation fixtures, and
  tests.
