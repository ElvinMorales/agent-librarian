# Catalog Format

The CLI produces three files under the selected output directory.

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

## Schemas

- [`catalog-entry.schema.json`](../schemas/catalog-entry.schema.json)
- [`catalog-index.schema.json`](../schemas/catalog-index.schema.json)
- [`overlap-report.schema.json`](../schemas/overlap-report.schema.json)

Schema version `0.1.0` describes the MVP output contract.
