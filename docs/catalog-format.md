# Catalog Format

The CLI produces four files under the selected output directory.

## `index.json`

The index contains deterministic source metadata and a list of catalog
entries. Each entry includes:

- identity: `id`, `name`, `artifact_type`, `source_path`
- classification: `taxonomy_bucket`, `framework_hint`
- discoverability: `description`, `purpose`, `activation_triggers`, `tags`
- contracts: `inputs`, `outputs`, `tool_scope`, `side_effects`, `dependencies`
- stewardship: `owner`, `version`, `related_files`
- review data: `public_safety_flags`, `discoverability_warnings`, `extraction`

Empty fields are preserved so missing contracts remain visible.

## `catalog.md`

The Markdown catalog is a review-oriented rendering of the same entries. It is
not a separate source of truth.

## `overlap-report.json`

Each candidate contains:

- `entry_ids`
- `overlap_type`
- `shared_terms`
- `confidence`
- `needs_human_review`
- `recommendation`

Confidence is a deterministic similarity indicator, not a probability or a
merge instruction.

## `diagnostics.json`

Diagnostics report inspectable parse outcomes without storing source file
contents. The top-level object contains:

- `schema_version`
- `source_root`
- `generated_at`: UTC generation time
- `summary`: counts for all four statuses
- `files`: one diagnostic for each non-ignored file seen by the scanner

Each file diagnostic contains:

- `source_path`: path relative to the scanned collection
- `status`: `parsed`, `partial`, `skipped`, or `failed`
- `parser`: `markdown`, `yaml`, `json`, or `null` for unsupported files
- `artifact_type_guess` and `taxonomy_bucket_guess`
- `warnings`: deterministic warning codes
- `error`: a sanitized parse error summary or `null`

Status meanings:

- `parsed`: the file was read and metadata was extracted without warnings.
- `partial`: useful metadata was extracted, but structure or important
  discoverability metadata was incomplete.
- `skipped`: the file type is unsupported and its contents were not read.
- `failed`: the file was selected for parsing but could not be read or parsed.

Normal mode records failures and continues. `--strict` writes diagnostics when
practical and exits non-zero when the summary contains one or more failed
files. Partial and skipped files do not cause strict-mode failure.

`generated_at` reflects the run time. Set `SOURCE_DATE_EPOCH` to a Unix
timestamp when reproducible generated output is required.

## Schemas

- [`catalog-entry.schema.json`](../schemas/catalog-entry.schema.json)
- [`catalog-index.schema.json`](../schemas/catalog-index.schema.json)
- [`overlap-report.schema.json`](../schemas/overlap-report.schema.json)
- [`diagnostics.schema.json`](../schemas/diagnostics.schema.json)

Schema version `0.1.0` describes the MVP output contract.
