# Architecture

`agent-librarian` is a deterministic file inspection pipeline:

```text
input directory
  -> safe scanner
  -> format parser and classifier
  -> per-file parse diagnostics
  -> normalized catalog entries
  -> warning rules
  -> pairwise overlap scoring
  -> JSON and Markdown renderers
  -> user-selected output directory
```

## Scanner

The scanner recursively inventories non-ignored files. Markdown, YAML, YML,
and JSON files are selected for parsing; unsupported files are recorded as
skipped without reading their contents. The scanner does not follow symbolic
links or enter common source-control, environment, dependency, cache, or
output directories. Selected files are read as text and are never imported,
sourced, evaluated, or executed.

## Parser and Classifier

Markdown parsing uses optional YAML frontmatter and heading-delimited sections.
YAML and JSON parsing uses structured parsers. Classification starts with
generic artifact classes and maps them to the stable taxonomy buckets.
Framework or protocol names are retained only as optional hints.

## Diagnostics

Each inventoried file receives a `parsed`, `partial`, `skipped`, or `failed`
status. Parse failures are isolated so normal mode can continue processing
other files. Error summaries include parser type and location where available,
but never source contents. Strict mode evaluates the completed diagnostics
report and exits non-zero if any file failed.

## Normalization

Different field names and heading forms are normalized into one catalog entry
model. Missing values remain empty and can produce discoverability warnings;
the tool does not invent contracts that are absent from source files.

## Warnings

Rules identify incomplete metadata, unclear action boundaries, broad tool
scope, absent examples or eval references, unknown artifacts, and text that
needs public-safety review. These rules are intentionally explainable and
conservative.

## Overlap

Entries of comparable types are tokenized and compared using deterministic
name and metadata overlap. Reports contain candidates and confidence values.
The CLI never automatically merges, deletes, or rewrites source artifacts.

## Outputs

Renderers create `index.json`, `catalog.md`, `overlap-report.json`, and
`diagnostics.json`. All writes are confined to the resolved `--out` directory.
