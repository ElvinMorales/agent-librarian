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

## Warning Reference

See [Warnings and overlap](warnings-and-overlap.md) for every active warning
code, suggested review actions, interpretation limits, and public-safety flag
meanings.

## `overlap-report.json`

Each candidate contains:

- `entry_ids`
- `overlap_type`
- `shared_terms`
- `confidence`
- `needs_human_review`
- `recommendation`

Confidence is a deterministic similarity indicator, not a probability or a
merge instruction. The exact formula, reporting thresholds, candidate types,
and synthetic examples are documented in
[Warnings and overlap](warnings-and-overlap.md#overlap-scoring).

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

- `parsed`: the file was read and metadata was extracted without structural or
  completeness warnings that make the result partial. Advisory review warnings
  can still be present.
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

## Validation

Validate a generated catalog directory with:

```bash
agent-librarian validate examples/generated-catalog
```

The command validates `index.json` and its embedded entries,
`overlap-report.json`, and `diagnostics.json` against the bundled schemas. It
prints a pass or failure for each file, exits non-zero when a required file is
missing, malformed, or schema-invalid, and does not modify generated files.
Validation is local and does not require network access.

Validation confirms generated JSON matches expected structure. It does not
certify that the catalog is complete, safe, semantically correct, or free of
private data.

## Offline HTML presentation

Render an existing generated catalog as a human-readable offline page:

```bash
agent-librarian present CATALOG_DIR --out OUT_DIR
```

The command reads `index.json`, `diagnostics.json`, and
`overlap-report.json` and writes `OUT_DIR/overview.html`. It does not read or
rescan the source collection. The HTML is self-contained, uses the catalog's
existing `generated_at` value, and is deterministic for unchanged input JSON.
Warnings and overlap candidates remain review prompts, not decisions.

Absence of validation errors or warning codes does not make an artifact
publication-ready. Public-safety review remains a human responsibility, and
generated catalogs from private collections must not be committed.

## Optional grounded narration

Install the optional provider dependency and explicitly opt in:

```bash
python -m pip install -e ".[narrate]"
agent-librarian present CATALOG_DIR --out OUT_DIR --narrate
agent-librarian present CATALOG_DIR --out OUT_DIR --narrate --model MODEL_ID
```

This path requires `ANTHROPIC_API_KEY` and contacts the Anthropic Messages API.
It sends only deterministic serializations of `index.json`,
`diagnostics.json`, and `overlap-report.json`; it does not rescan sources or
read other repository files. A narrated run writes:

- `overview.html`: model-authored narrative near the top, followed by the
  deterministic catalog facts.
- `narrative.md`: the labeled model-authored narrative.
- `narrative-provenance.json`: model ID, UTC creation time, allowed input file
  names, token usage, and a SHA-256 digest.

The digest is calculated over the exact canonical JSON string sent as the
single user-message payload. The provenance file does not contain source file
contents. All three outputs are staged only after a successful model response.
The narrative is a secondary review aid, not a decision or certification.
