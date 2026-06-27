# v0.6.0 Release Checklist

The maintainer performs tag creation and GitHub release publication manually
after this checklist passes. This release does not include PyPI publishing.

## Release notes draft

```text
v0.6.0 — Presentation Layer

This release adds a human-readable presentation layer for generated artifact
catalogs.

Highlights:
- deterministic offline `present` command
- self-contained `overview.html`
- optional grounded `--narrate` mode
- `narrative.md` and `narrative-provenance.json`
- synthetic presentation demos
- walkthrough and safety docs for reviewing presentation outputs

Boundary:
- default CLI remains offline and deterministic
- narration is explicit opt-in and provider-backed
- generated presentation outputs inherit source sensitivity
- model narrative is a secondary review aid, not certification
```

## Pre-release checks

- Confirm the release branch starts from an updated, clean `main`.
- Confirm the change set contains release metadata and documentation only.
- Confirm there are no runtime behavior, provider behavior, or output schema
  changes.
- Confirm no schema versions changed without an explicit schema contract
  change.
- Confirm `agent/`, `packages/`, and `examples/generated-catalog/` are
  unchanged.
- Confirm committed generated presentation demos are unchanged unless a
  release version was intentionally embedded and required an update.
- Confirm all committed examples remain synthetic and public-safe.

## Version and changelog

- Confirm `pyproject.toml` reports `0.6.0`.
- Confirm `src/agent_librarian/__init__.py` reports `0.6.0`.
- Confirm `agent-librarian --version` prints exactly
  `agent-librarian 0.6.0`.
- Confirm `CHANGELOG.md` contains the dated `0.6.0` release entry.
- Confirm internal catalog schema versions remain unchanged.

## Validation commands

Run from the repository root:

```bash
python -m pip install -e ".[dev]"
agent-librarian --version
agent-librarian --help
agent-librarian present --help
agent-librarian catalog examples/sample-collection --out .tmp/generated-catalog
agent-librarian validate .tmp/generated-catalog
agent-librarian report .tmp/generated-catalog
agent-librarian present examples/generated-catalog --out .tmp/present-demo
python scripts/check_packages.py
pytest
git diff --check
git diff --exit-code -- examples/generated-catalog
```

Expected results:

- `agent-librarian --version` prints exactly `agent-librarian 0.6.0`.
- Help commands exit successfully and list the expected bounded CLI options.
- Catalog generation writes the four deterministic catalog files under
  `.tmp/generated-catalog`.
- Validation reports all generated JSON documents as valid.
- Report and offline presentation generation exit successfully.
- `.tmp/present-demo/overview.html` exists.
- Package conformance and all tests pass.
- Whitespace validation passes and committed generated catalog fixtures have
  no diff.

## Committed presentation demo checks

PowerShell:

```powershell
Test-Path examples/generated-presentation/overview.html
Test-Path examples/generated-presentation/README.md
Test-Path examples/generated-presentation-narrated/overview.html
Test-Path examples/generated-presentation-narrated/narrative.md
Test-Path examples/generated-presentation-narrated/narrative-provenance.json
Test-Path examples/generated-presentation-narrated/README.md
python -m json.tool examples/generated-presentation-narrated/narrative-provenance.json | Out-Null
```

Bash:

```bash
test -f examples/generated-presentation/overview.html
test -f examples/generated-presentation/README.md
test -f examples/generated-presentation-narrated/overview.html
test -f examples/generated-presentation-narrated/narrative.md
test -f examples/generated-presentation-narrated/narrative-provenance.json
test -f examples/generated-presentation-narrated/README.md
python -m json.tool examples/generated-presentation-narrated/narrative-provenance.json > /dev/null
```

Confirm every file check succeeds, the narrated provenance parses as JSON,
`model` is `synthetic-static-stub`, and both `input_tokens` and
`output_tokens` are `0`.

Do not run a real provider call for release validation unless intentionally
testing the optional online path in a private/local context.

## Safety and boundary checks

- Confirm `catalog`, `validate`, `report`, and default `present` remain the
  deterministic offline core.
- Confirm `present --narrate` remains an explicit optional online
  presentation aid.
- Confirm deterministic generated facts remain the source of truth and model
  narrative is described only as a secondary review aid.
- Confirm presentation outputs inherit source sensitivity and public demos
  use only synthetic data.
- Confirm no real provider/model call was made during normal release
  validation.
- Confirm release text does not claim SharePoint, Microsoft 365, Graph, MCP,
  source crawling, connectors, multi-provider narration, or compliance
  certification.

## CI status check

- Confirm release branch CI passes before merge.
- Confirm CI runs tests, whitespace checks, generated-output cleanliness, and
  package conformance checks.

## Tag and release steps

Tag creation and GitHub release publication are maintainer-only follow-up
steps after local validation, review, merge, and CI pass:

1. Review and merge the release change through the normal repository process.
2. Pull the merged `main` branch.
3. Create and push the annotated `v0.6.0` tag.
4. Publish the GitHub release using the release notes draft above and the
   `CHANGELOG.md` `0.6.0` section.
5. Leave package registry publishing out of scope unless separately approved.

## Post-release checks

- Confirm the GitHub release points to the intended `v0.6.0` tag.
- Confirm the release text preserves the offline/online boundary,
  sensitivity inheritance, deterministic source-of-truth status, and
  non-certification language.
- Confirm no package registry artifact was published.
