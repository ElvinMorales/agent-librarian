# v0.5.0 Release Checklist

The maintainer performs tag creation and GitHub release publication manually
after this checklist passes. This release does not include PyPI publishing.

Release description:

```text
v0.5.0 — Portable LLM Agent Packages
```

## Pre-release checks

- Confirm the release branch starts from an updated, clean `main`.
- Confirm the change set contains release metadata, documentation, package
  manifest, and CI hygiene only.
- Confirm there are no runtime behavior changes, deterministic schema
  changes, provider integrations, MCP server code, network behavior, or new
  package families.
- Confirm generated examples remain synthetic and unchanged unless validation
  proves they are stale.
- Confirm package examples and docs contain no employer-specific examples,
  private data, secrets, credentials, private scans, generated private
  outputs, traces, logs, memory snapshots, or state snapshots.

## Version and changelog

- Confirm `pyproject.toml` reports `0.5.0`.
- Confirm `src/agent_librarian/__init__.py` reports `0.5.0`.
- Confirm `agent-librarian --version` prints `0.5.0`.
- Confirm `CHANGELOG.md` contains the dated `0.5.0` release entry.
- Confirm internal schema versions remain unchanged unless their schema
  contracts changed.

## Package and docs checks

- Confirm `packages/shared/package-manifest.example.yaml` references the
  shared package foundation, Claude package, OpenAI/Codex package, GPT
  package, ChatGPT Project package, demo docs, conformance checker, and pytest
  coverage.
- Confirm `python scripts/check_packages.py` passes.
- Confirm package conformance tests pass through `pytest`.
- Confirm static package docs preserve source-of-truth, exact approval,
  advisory-only, public-safety, and non-certification boundaries.
- Confirm GPT and ChatGPT Project docs do not claim local command execution.
- Confirm Claude Code and Codex docs describe local commands only through
  approval-gated workflows.

## Validation commands

Run from the repository root:

```bash
python -m pip install -e ".[dev]"
agent-librarian --version
agent-librarian --help
agent-librarian validate examples/generated-catalog
agent-librarian report examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose catalog examples/sample-collection --out examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose validate examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose report examples/generated-catalog
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "wrong command"
python -m json.tool agent/schemas/review-summary.schema.json
python -m json.tool agent/schemas/review-summary.example.json
python -m json.tool packages/shared/package-manifest.schema.json
python scripts/check_packages.py
pytest
git diff --check
git diff --exit-code -- examples/generated-catalog
```

The wrong-command approval check is expected to fail with a nonzero exit
status. It must report an approval mismatch and must not execute the
deterministic backend.

Also parse YAML manifests:

```bash
python -c "from pathlib import Path; import yaml; yaml.safe_load(Path('packages/shared/package-manifest.example.yaml').read_text(encoding='utf-8')); yaml.safe_load(Path('agent/tools/tools.yaml').read_text(encoding='utf-8')); print('yaml: valid')"
```

## Public-safety checks

Run the static sweep:

```bash
rg -n "employer|internal URL|credential|secret|private prompt|private trace|memory snapshot|state snapshot|journal|client data|work folder" README.md docs packages agent examples scripts tests
```

The sweep may find safety warnings. Confirm matches are generic warnings or
synthetic placeholders only, not real private or employer-specific content.

Confirm:

- No private paths.
- No employer-specific examples.
- No secrets or credentials.
- No private prompts, traces, logs, memory snapshots, or state snapshots.
- No generated private catalogs.
- No claims of employer endorsement.
- Validation, reports, package conformance, and review summaries are not
  described as safety, correctness, completeness, approval, compliance, or
  publication certification.

## CI status check

- Confirm the release branch CI passes before merge.
- Confirm CI runs tests, whitespace checks, generated-output cleanliness, and
  package conformance checks.

## Tag and release steps

Tag creation and GitHub release publication are maintainer-only follow-up
steps after local validation, review, merge, and CI pass:

1. Review and merge the release change through the normal repository process.
2. Pull the merged `main` branch.
3. Create and push the annotated `v0.5.0` tag.
4. Publish the GitHub release using the `CHANGELOG.md` `0.5.0` section.
5. Leave package registry publishing out of scope unless separately approved.

## Post-release checks

- Confirm the GitHub release points to the intended `v0.5.0` tag.
- Confirm the release text preserves deterministic CLI, package adapter, local
  approval, advisory-only, and public-safety boundaries.
- Confirm no package registry artifact was published.
