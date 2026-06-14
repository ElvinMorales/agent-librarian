# agent-librarian

`agent-librarian` is a deterministic, local-only CLI for cataloging collections
of agentic AI artifacts. It scans Markdown, YAML, and JSON files; classifies
them with a framework-neutral taxonomy; extracts discoverability metadata; and
reports likely overlap without modifying or executing the source collection.

The MVP is intended for public-safe collections of skills, agents, prompts,
tool specifications, schemas, and protocol-facing manifests.

For a short project framing and demo-safe overview, see the
[Showcase Brief](docs/showcase-brief.md).

For a runnable five-minute demo path, see the
[Demo Walkthrough](docs/demo-walkthrough.md).

For a live presentation path, see the
[Forum Demo Runbook](docs/forum-demo-runbook.md).

For a taxonomy-aligned view of the system, see the
[Architecture Map](docs/taxonomy-architecture-map.md).

For guidance on safely adapting the tool to your own collection, see the
[Public-Safe Adoption Guide](docs/adoption-guide.md).

## Quickstart

```bash
python -m pip install -e ".[dev]"
agent-librarian --help
agent-librarian catalog examples/sample-collection --out examples/generated-catalog
agent-librarian catalog examples/sample-collection --out examples/generated-catalog --strict
agent-librarian validate examples/generated-catalog
pytest
```

The `catalog` command creates:

- `index.json`: machine-readable catalog entries and generation metadata.
- `catalog.md`: a human-readable inventory with warnings.
- `overlap-report.json`: duplicate and overlap candidates for human review.
- `diagnostics.json`: per-file parse status, warning codes, and sanitized errors.

The CLI parses only supported files under the input directory and records
unsupported non-ignored files as skipped without reading their contents. It
applies safe default excludes for Git metadata, environment and dependency
folders, caches, build outputs, and generated catalogs. The selected output
directory is also excluded whenever it is inside the input directory. It
writes only the four generated files under `--out`.

### Scan Include and Exclude Patterns

Narrow the inventoried files with repeated `--include` glob patterns and add
custom relative path or name exclusions with `--exclude`:

```bash
agent-librarian catalog ./collection --out ./catalog \
  --include "**/*.md" \
  --include "**/*.yaml" \
  --exclude "private, scratch, tmp"
```

Include patterns narrow what appears in the scan and diagnostics. Repeated
include patterns are combined with OR. Exclude values may be comma-separated
or repeated, and custom excludes always add to the safe defaults.

Use include and exclude patterns to keep private folders, raw traces,
memory/state snapshots, credentials, and generated outputs out of public
catalogs. Generated catalogs from private collections should not be committed.

Normal mode continues when an individual file cannot be parsed, omits failed
files from the catalog entries, records the failure in `diagnostics.json`, and
exits `0` unless the command itself fails. Add `--strict` for CI or release
validation:

```bash
agent-librarian catalog COLLECTION --out GENERATED --strict
```

Strict mode still writes outputs when practical, then exits non-zero if any
file has a `failed` parse status. Partial and skipped files do not make strict
mode fail.

Validate generated JSON against the bundled catalog schemas:

```bash
agent-librarian validate examples/generated-catalog
```

The command checks `index.json`, its embedded catalog entries,
`overlap-report.json`, and `diagnostics.json`. It reports each file as passing
or failing and exits non-zero for missing, malformed, or schema-invalid JSON.
Validation is read-only and requires no network access.

Validation confirms generated JSON matches expected structure. It does not
certify that the catalog is complete, safe, semantically correct, or free of
private data.

After generating a catalog, summarize the review surfaces:

```bash
agent-librarian report examples/generated-catalog
```

The report reads existing generated outputs and summarizes diagnostics,
warnings, and overlap candidates for human review. It does not rescan source
files, modify generated outputs, or make artifact-management decisions.

## What It Catalogs

The classifier recognizes common artifact surfaces such as:

- `SKILL.md` capability modules
- `AGENTS.md`, `CLAUDE.md`, and agent manifests
- prompt Markdown files
- tool manifests
- MCP-style JSON manifests
- JSON Schemas

Internal classification uses the stable 14-bucket framework documented in
[taxonomy alignment](docs/taxonomy-alignment.md). Framework and protocol names
are optional hints, not replacement taxonomy categories.

## Metadata and Warnings

Markdown frontmatter, headings, YAML fields, and JSON fields are normalized
into catalog entries. Entries can include purpose, activation triggers, inputs,
outputs, tool scope, side effects, dependencies, tags, ownership, version,
related files, safety flags, discoverability warnings, and extraction
confidence.

Warnings identify missing or weak metadata, unclear output contracts, broad
tool scope, unclear side effects, missing examples or evals, unknown artifact
types, and overlap candidates. Warnings are review aids, not correctness or
safety certifications.

See [Warnings and overlap](docs/warnings-and-overlap.md) for warning code
meanings, suggested review actions, diagnostics interpretation, and the exact
overlap scoring thresholds.

## Non-Goals

Version `0.1.0` is not:

- a marketplace or hosted registry
- a web application
- an agent runtime or framework
- an LLM-powered reviewer
- a protocol validator
- an automatic merge or deduplication tool
- a scanner for live memory, runtime state, logs, or traces

## Public Safety

All committed examples are synthetic. Do not catalog or publish secrets,
credentials, private endpoints, employer-specific workflows, real user data,
live memory stores, raw traces, or unsanitized runtime state without an
appropriate private handling and review process.

See [public-safety guidance](docs/public-safety.md) and the
[sample collection](examples/README.md).

## Development

```bash
python -m pip install -e ".[dev]"
pytest
git diff --check
```

See [Developer workflow](docs/developer-workflow.md) for local setup,
validation commands, branch hygiene, Codex handoff expectations, and
public-safety reminders.

The project does not call external services and requires no API keys.
