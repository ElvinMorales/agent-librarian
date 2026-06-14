# agent-librarian

`agent-librarian` is a deterministic, local-only CLI for cataloging collections
of agentic AI artifacts. It scans Markdown, YAML, and JSON files; classifies
them with a framework-neutral taxonomy; extracts discoverability metadata; and
reports likely overlap without modifying or executing the source collection.

The MVP is intended for public-safe collections of skills, agents, prompts,
tool specifications, schemas, and protocol-facing manifests.

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
ignores `.git`, `.env`, `.venv`, `node_modules`, `__pycache__`, and the selected
output directory. It writes only the four generated files under `--out`.

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

Normal `pytest` is the default for local development and CI. On Windows, use
the following workaround only if `pytest` fails because it cannot create or
access its default local temp or cache directories:

```powershell
New-Item -ItemType Directory -Force .pytest-tmp | Out-Null
pytest --basetemp .\.pytest-tmp -p no:cacheprovider
```

The `.pytest-tmp/` and `.tmp/` directories are local-only troubleshooting
folders and should not be committed.

GitHub Actions runs these checks on Python 3.10, 3.11, and 3.12. It also
regenerates and validates the synthetic sample catalog with a fixed
`SOURCE_DATE_EPOCH`, then fails if the committed generated outputs differ.

The project does not call external services and requires no API keys.
