# Changelog

All notable changes to this project are documented here.

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
