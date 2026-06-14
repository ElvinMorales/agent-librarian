# Developer Workflow

This guide describes the expected local workflow for contributors and Codex
runs. Keep changes focused, preserve deterministic generated outputs, and use
only synthetic public-safe examples.

## Local Setup

Install the package and development dependencies, then confirm the CLI is
available:

```bash
python -m pip install -e ".[dev]"
agent-librarian --help
```

## Normal Validation Loop

Regenerate and validate the synthetic sample catalog before running the test
and whitespace checks:

```bash
agent-librarian catalog examples/sample-collection --out examples/generated-catalog
agent-librarian validate examples/generated-catalog
pytest
git diff --check
```

Validation confirms generated JSON matches the expected schema. It does not
certify that a catalog is complete, safe, semantically correct, or free of
private data.

## Deterministic Generated Output

CI sets:

```bash
SOURCE_DATE_EPOCH=1781481600
```

This fixes generated timestamps so CI can enforce that the committed synthetic
sample outputs stay current. On shells that support inline environment
variables, reproduce the check with:

```bash
SOURCE_DATE_EPOCH=1781481600 agent-librarian catalog examples/sample-collection --out examples/generated-catalog
agent-librarian validate examples/generated-catalog
git diff --exit-code -- examples/generated-catalog
```

In Windows PowerShell, use:

```powershell
$env:SOURCE_DATE_EPOCH = "1781481600"
agent-librarian catalog examples/sample-collection --out examples/generated-catalog
agent-librarian validate examples/generated-catalog
git diff --exit-code -- examples/generated-catalog
```

## Windows Pytest Troubleshooting

Normal `pytest` remains the default for local development and CI. Use this
workaround only when local Windows temp or cache permissions prevent pytest
from running normally:

```powershell
New-Item -ItemType Directory -Force .pytest-tmp | Out-Null
pytest --basetemp .\.pytest-tmp -p no:cacheprovider
```

The `.pytest-tmp/` and `.tmp/` directories are ignored and must remain
local-only.

## Branch Workflow

Start from an up-to-date `main` branch and create a focused issue branch:

```bash
git checkout main
git pull --ff-only origin main
git checkout -b type/issue-number-short-description
```

Examples:

```text
docs/issue-17-developer-workflow-codex-handoff
test/issue-14-github-actions-ci
chore/issue-16-windows-pytest-temp-handling
feature/issue-15-schema-validation-command
```

## Commit Messages

Use a conventional type followed by a concise description:

```text
type: concise description
```

Examples:

```text
feat: add catalog schema validation command
test: add GitHub Actions CI
chore: improve Windows pytest temp handling
docs: add developer workflow and Codex handoff guidance
```

When a commit should close an issue, include the issue reference in the commit
body:

```text
Closes #17
```

## Pull Request Expectations

- Open pull requests into `main`.
- Keep each pull request focused on one issue or cohesive change.
- List the validation commands run in the pull request description.
- Keep documentation, tests, and generated examples synthetic.
- Delete merged branches.
- Do not push directly to `main` unless a repository administrator is
  intentionally bypassing branch rules.

## Codex Handoff Checklist

At the end of a Codex run, summarize:

- issue number
- files changed
- behavior changed
- documentation changed
- tests added or changed
- validation commands run
- CI status, if available
- generated outputs changed, if any
- public-safety review notes
- risks or TODOs
- recommended next issue

## Public-Safety Reminder

Do not commit:

- secrets
- credentials
- private prompts
- private generated catalogs
- real trace logs
- real memory or state snapshots
- employer-specific examples
- internal URLs
- private local paths
- real user data

Use only synthetic examples in public documentation and tests. Review both
source artifacts and generated outputs before publishing them.
