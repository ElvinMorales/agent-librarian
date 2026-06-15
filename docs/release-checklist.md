# v0.4.0 Release Checklist

The maintainer performs tag creation and GitHub release publication manually
after this checklist passes. This release does not include PyPI publishing.

## Pre-release checks

- Confirm the release branch starts from an updated, clean `main`.
- Confirm the change set contains release metadata, documentation, and CI
  hygiene only.
- Confirm the stable deterministic CLI remains the source of truth.
- Confirm the optional runtime wrapper remains local-only, approval-gated, and
  bounded to documented `catalog`, `validate`, and `report` actions.
- Confirm generated examples remain synthetic and unchanged.
- Open external PR #62 is outside the v0.4 release scope and should be reviewed
  separately after the release, or closed as not planned if it does not fit
  the project's contribution or safety standards.

## Version and changelog

- Confirm `pyproject.toml` reports `0.4.0`.
- Confirm `src/agent_librarian/__init__.py` reports `0.4.0`.
- Confirm `agent-librarian --version` prints `0.4.0`.
- Confirm `CHANGELOG.md` contains the dated `0.4.0` release entry.
- Confirm current-version documentation does not describe v0.3 as current.

## Validation commands

Run from the repository root:

```bash
python -m pip install -e ".[dev]"
agent-librarian --version
agent-librarian --help
agent-librarian catalog --help
agent-librarian catalog examples/sample-collection --out examples/generated-catalog
agent-librarian validate examples/generated-catalog
agent-librarian report examples/generated-catalog
python -m json.tool agent/schemas/review-summary.schema.json
python -m json.tool agent/schemas/review-summary.example.json
pytest
git diff --check
git diff --exit-code -- examples/generated-catalog
```

Also parse the tool manifest:

```bash
python -c "from pathlib import Path; import yaml; yaml.safe_load(Path('agent/tools/tools.yaml').read_text(encoding='utf-8')); print('tools yaml: valid')"
```

If normal catalog regeneration creates timestamp-only noise, rerun the
deterministic check in PowerShell:

```powershell
$env:SOURCE_DATE_EPOCH = "1781481600"
agent-librarian catalog examples/sample-collection --out examples/generated-catalog
agent-librarian validate examples/generated-catalog
git diff --exit-code -- examples/generated-catalog
agent-librarian report examples/generated-catalog
```

## Runtime-wrapper smoke checks

```bash
python -m agent_librarian.runtime_wrapper propose catalog examples/sample-collection --out examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose validate examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose report examples/generated-catalog
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "wrong command"
```

The wrong-command approval check is expected to fail with a nonzero exit
status. It must report an approval mismatch and must not execute the
deterministic backend.

## Public-safety checks

- No private paths.
- No employer-specific examples.
- No secrets or credentials.
- No private prompts, traces, logs, memory snapshots, or state snapshots.
- No generated private catalogs.
- No claims of employer endorsement.
- External PR #62 is not included in v0.4 unless separately reviewed.
- Validation, reports, and review summaries are not described as safety,
  correctness, completeness, approval, or publication certification.

## GitHub release steps

After local validation and release-branch CI pass, the maintainer:

1. Reviews and merges the release change through the normal repository process.
2. Pulls the merged `main` branch.
3. Creates and pushes the annotated `v0.4.0` tag.
4. Publishes the GitHub release using the `CHANGELOG.md` `0.4.0` section.
5. Leaves package registry publishing out of scope unless separately approved.

## Post-release checks

- Confirm the GitHub release points to the intended `v0.4.0` tag.
- Confirm the release text preserves the runtime and public-safety boundaries.
- Confirm no package registry artifact was published.
- Confirm PR #62 remains separate from the v0.4 release and has not been
  implicitly accepted by the release.
