# Synthetic SharePoint-Style End-to-End Demo

This public-safe demo simulates a SharePoint-style source by using only the
fabricated files already committed under
`examples/source-snapshots/synthetic-team-space`. It runs locally without
Microsoft credentials or network access.

This is a synthetic simulation of the snapshot boundary. It does not connect
to SharePoint or Microsoft 365, exercise a live exporter, or prove that a live
connector is ready, safe, complete, compliant, approved, or publishable.

## Responsibility boundary

```text
synthetic SharePoint-style source
  -> local files/ + source-manifest.json
  -> source snapshot conformance check
  -> agent-librarian catalog
  -> validate / report / present
  -> optional Claude Code review of local deterministic outputs
```

The companion
[`agent-librarian-m365-snapshot-adapter`](https://github.com/ElvinMorales/agent-librarian-m365-snapshot-adapter)
repository is the future home for provider-specific Microsoft 365 export
behavior. An adapter is responsible for approved, read-only provider access and
for writing a compatible local snapshot and manifest.

The core `agent-librarian` repository remains local-first and provider-neutral.
It owns the source snapshot contract, offline conformance check, and local
`catalog`, `validate`, `report`, and `present` commands. This demo starts after
the source-to-snapshot boundary and does not exercise a live connector.

## Synthetic input

The committed fixture has this shape:

```text
examples/source-snapshots/synthetic-team-space/
|-- source-manifest.json
`-- files/
    |-- Policies/public-safety-notes.md
    `-- Prompts/catalog-review-prompt.md
```

The manifest records fabricated source provenance, approved and excluded
scope, file sizes and SHA-256 digests, public-synthetic sensitivity, and review
notes. The `files/` directory is the catalog input; the adjacent manifest is
provenance and is not cataloged.

In a future live workflow, the companion adapter would create this boundary
artifact. For this demo, the snapshot is hand-authored and committed so every
step remains offline and reproducible.

## Prerequisite

From the repository root, install the project if the CLI is not already
available:

```bash
python -m pip install -e ".[dev]"
```

The remaining commands read only committed synthetic inputs and write only
under the ignored `.tmp/` directory.

## 1. Check source snapshot conformance

```bash
python scripts/check_source_snapshot.py examples/source-snapshots/synthetic-team-space
```

The check validates the manifest schema, path containment, listed file
existence, byte sizes, SHA-256 digests, unlisted files, and targeted obvious
leakage markers for public examples. A pass proves only those bounded checks;
it is not a safety or publication certificate.

## 2. Catalog the local snapshot files

```bash
agent-librarian catalog examples/source-snapshots/synthetic-team-space/files --out .tmp/synthetic-sharepoint-catalog --strict
```

The command reads the two synthetic Markdown files and writes these local
deterministic review artifacts:

```text
.tmp/synthetic-sharepoint-catalog/
|-- index.json
|-- catalog.md
|-- overlap-report.json
`-- diagnostics.json
```

## 3. Validate, report, and present

```bash
agent-librarian validate .tmp/synthetic-sharepoint-catalog
agent-librarian report .tmp/synthetic-sharepoint-catalog
agent-librarian present .tmp/synthetic-sharepoint-catalog --out .tmp/synthetic-sharepoint-presentation
```

`validate` checks the generated JSON artifacts against their schemas. `report`
prints catalog counts, parser status, warnings, and overlap candidates for
human review. `present` renders the same generated facts to:

```text
.tmp/synthetic-sharepoint-presentation/overview.html
```

For the current fixture, the report identifies two catalog entries, two
partial parses, no failed files, and no overlap candidates. Warnings and parse
status are review prompts, not conclusions. Inspect `diagnostics.json`,
`catalog.md`, `index.json`, and `overlap-report.json` before interpreting the
result.

## 4. Optional Claude Code review

Use this prompt only after the commands above succeed. It is for this synthetic
demo; private-source handling remains covered by the
[Claude Code private-source snapshot runbook](claude-code-private-source-snapshot.md).

```text
Review only these generated local paths:
- catalog: .tmp/synthetic-sharepoint-catalog
- presentation: .tmp/synthetic-sharepoint-presentation

This is a synthetic SharePoint-style demo. Do not access external sources.
Do not access SharePoint or Microsoft 365. Do not make network requests. Do
not inspect paths outside the two generated locations above.

Summarize deterministic outputs only: index.json, diagnostics.json,
overlap-report.json, catalog.md, and overview.html. Separate facts emitted by
the CLI from your interpretation. Treat warnings and overlap candidates as
review prompts, not decisions. Do not claim safety, privacy, correctness,
completeness, compliance, approval, or publication readiness.
```

Claude Code's summary is optional and secondary. The generated local files and
CLI output remain the source of truth.

## Cleanup

Remove the ignored demo outputs when finished:

```powershell
Remove-Item -Recurse -Force .tmp\synthetic-sharepoint-catalog, .tmp\synthetic-sharepoint-presentation -ErrorAction SilentlyContinue
```

Do not replace the synthetic fixture with private exports or commit generated
outputs from a private snapshot.
