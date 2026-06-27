# Public-Safe Adoption Guide

## Purpose

This guide explains how to adapt `agent-librarian` to a local artifact
collection while keeping private work separate from public repository
examples. Treat personal, employer, client, customer, and other non-public
collections as private by default.

The deterministic `catalog`, `validate`, `report`, and default `present` paths
run locally and do not execute scanned artifacts or call an LLM or network
service. The explicit optional `present --narrate` path contacts Anthropic.
These boundaries do not make source files or generated outputs safe to
publish. Human review remains required.

The CLI-generated files remain the source of truth. Optional model narrative
is a secondary review aid and cannot certify safety, privacy, correctness,
completeness, compliance, approval, or publication readiness.

## Start with the synthetic example

Learn the workflow with the fabricated, public-safe files in
`examples/sample-collection`. From the repository root, run:

```bash
python -m pip install -e ".[dev]"
agent-librarian catalog examples/sample-collection --out examples/generated-catalog
agent-librarian validate examples/generated-catalog
agent-librarian report examples/generated-catalog
agent-librarian present examples/generated-catalog --out .tmp/present-demo
```

Inspect the source collection and the four files under
`examples/generated-catalog`. These committed examples are intentionally
created for public use and demonstrate diagnostics, warnings, and overlap
review without exposing a real collection.

## Before scanning your own collection

Inventory the intended source area before running the CLI. Remove or exclude
material that does not belong in the scan, including private folders, raw
traces, scratch areas, temporary files, memory or state snapshots, credentials,
and generated outputs.

Decide whether every selected file is appropriate for the people who can
access the local output directory. A local scan can still copy names, relative
paths, metadata, warning codes, and review findings into generated files.

## Choose a private local workspace

Keep both the source collection and generated catalog in private local
locations outside a public repository. Use placeholder paths in shared
documentation and examples rather than real workspace locations.

For private local use:

```bash
agent-librarian catalog path/to/private-artifact-collection --out path/to/private-generated-catalog
agent-librarian validate path/to/private-generated-catalog
agent-librarian report path/to/private-generated-catalog
```

Do not commit `path/to/private-generated-catalog` or copy its files into the
public example directory.

## Use include and exclude patterns deliberately

Use `--include` to narrow the scan to intended file patterns:

```bash
agent-librarian catalog path/to/private-artifact-collection --out path/to/private-generated-catalog --include "**/*.md"
```

Use `--exclude` to add private or irrelevant names and paths to the built-in
safe defaults:

```bash
agent-librarian catalog path/to/private-artifact-collection --out path/to/private-generated-catalog --exclude "private,scratch,tmp,traces"
```

Include patterns are combined with OR when repeated. Exclude values may be
comma-separated or repeated, and custom excludes add to the built-in defaults.
Review the selected scope before scanning. Patterns reduce accidental
collection, but they are not a privacy or publication-safety guarantee.

## Generate outputs locally

Run catalog generation on the machine and in the private workspace where the
collection is stored. The CLI writes `index.json`, `catalog.md`,
`overlap-report.json`, and `diagnostics.json` under the selected `--out`
directory.

Choose an output directory that is not synchronized, published, or tracked by
a public repository. Confirm the directory's access and backup behavior if the
collection contains sensitive material.

## Present catalogs with the same sensitivity boundary

The default presentation path is offline, deterministic, provider-free, and
requires no API key:

```bash
agent-librarian present path/to/private-generated-catalog --out path/to/private-presentation
```

Its `overview.html` can contain artifact names, relative paths, diagnostics,
warnings, and overlap findings. It inherits the catalog's sensitivity and must
remain private when the catalog is private.

Narration is a separate, explicit opt-in path:

```bash
python -m pip install -e ".[narrate]"
agent-librarian present path/to/private-generated-catalog --out path/to/private-narrated-presentation --narrate
```

It requires `ANTHROPIC_API_KEY` and sends deterministic serializations of
`index.json`, `diagnostics.json`, and `overlap-report.json` to Anthropic. Use it
only when sending that generated metadata to the configured provider is
acceptable. The resulting narrative may repeat sensitive artifact names,
paths, warnings, and overlap information.

Do not commit or publicly share `overview.html`, `narrative.md`, or
`narrative-provenance.json` generated from a private catalog. Public demos must
use intentionally synthetic catalog data.

## Validate and report before reviewing

After each catalog run, validate the generated JSON and summarize the review
surfaces:

```bash
agent-librarian validate path/to/private-generated-catalog
agent-librarian report path/to/private-generated-catalog
```

Validation checks generated JSON structure. The report summarizes diagnostics,
warnings, and overlap candidates. Neither command certifies completeness,
semantic correctness, privacy, safety, or publication readiness.

Use the report to orient the review, then inspect the generated files and the
corresponding source artifacts.

## Review generated outputs before sharing

Review both the selected source artifacts and every generated output before
sharing anything. Check names, paths, descriptions, metadata, diagnostics,
warning codes, overlap findings, and error summaries for contextual
disclosure.

A generated catalog is not automatically public-safe just because the tool
created it. It may contain names, paths, metadata, warning codes, or review
findings from the scanned collection.

Absence of validation errors or public-safety warnings does not prove that the
source or generated files are safe to publish.

The same rule applies to the optional narrated presentation. A model narrative
does not certify safety, privacy, correctness, completeness, compliance,
approval, or publication readiness, and it does not replace review of the
private source collection and generated files.

## What is safe to commit

Commit examples only when they are:

- synthetic and intentionally created for public use
- clearly separated from private local collections
- reviewed source files
- reviewed generated outputs
- free of private paths, credentials, secrets, real traces, internal URLs,
  and regulated or private data

The repository's `examples/sample-collection` and
`examples/generated-catalog` demonstrate this standard. Do not replace or mix
them with files from a private scan.

## What not to publish

Do not publish:

- private prompts
- real traces
- memory or state snapshots
- source files from private projects
- generated catalogs from private scans
- credentials
- secrets
- API keys
- internal URLs
- employer workflows
- customer or user data
- regulated or private data
- proprietary schemas or manifests
- screenshots of private or internal systems

This list is not exhaustive. When ownership, consent, classification, or
publication rights are unclear, keep the material private.

## Adoption checklist

- [ ] Start with `examples/sample-collection`.
- [ ] Treat the real collection as private by default.
- [ ] Keep source and output paths in a private local workspace.
- [ ] Use placeholder paths in shared commands and documentation.
- [ ] Narrow the scan with deliberate `--include` patterns.
- [ ] Exclude private folders, traces, scratch areas, temporary files, state,
      and generated outputs.
- [ ] Run `validate` and `report` after generating the catalog.
- [ ] Keep presentation outputs private whenever the source catalog is private.
- [ ] Use `--narrate` only when provider disclosure of generated metadata is
      acceptable.
- [ ] Review both source artifacts and all generated outputs.
- [ ] Keep public examples synthetic and intentionally public.
- [ ] Do not commit generated catalogs from private collections.
- [ ] Confirm no credentials, secrets, private paths, internal URLs, or
      regulated or private data are present before sharing.

## Related docs

- [Project overview](../README.md)
- [Synthetic example collection](../examples/README.md)
- [Demo walkthrough](demo-walkthrough.md)
- [Presentation demo walkthrough](presentation-demo-walkthrough.md)
- [Public safety](public-safety.md)
- [Catalog format](catalog-format.md)
- [Warnings and overlap](warnings-and-overlap.md)
- [Architecture](architecture.md)
