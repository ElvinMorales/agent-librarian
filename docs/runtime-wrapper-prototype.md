# Local Runtime Wrapper Prototype

## Purpose

Issue
[#52](https://github.com/ElvinMorales/agent-librarian/issues/52)
adds an optional local approval-gated harness around the deterministic
`agent-librarian` CLI backend.

The prototype demonstrates this bounded sequence:

```text
explicit request input
  -> scope and sensitivity check
  -> exact command proposal
  -> exact approval gate
  -> deterministic CLI backend execution
  -> optional runtime, approval, and execution records
  -> optional review-summary handoff shape
```

This prototype is not an autonomous LLM agent. It does not call an LLM
provider. It does not add network behavior. It does not expose arbitrary shell
execution. It is a local approval-gated harness around the deterministic CLI
backend.

## Status and Boundaries

The module is available through:

```text
python -m agent_librarian.runtime_wrapper
```

It is intentionally separate from the stable `agent-librarian` console
script. The existing `catalog`, `validate`, and `report` commands remain
directly usable and remain the source of truth.

The wrapper implements a narrow part of the designs in:

- [CLI tool contract](../agent/tools/agent-librarian-cli.md)
- [Catalog-review workflow](../agent/workflows/catalog-review.md)
- [LLM-layer public-safety policy](../agent/policies/public-safety.md)
- [Safe-scan eval cases](../agent/evals/safe-scan-cases.md)
- [Runtime state and approval records](../agent/runtime/state-and-approval-log.md)
- [Review summary schema](../agent/schemas/review-summary.schema.json)

## Supported Actions

Only these command forms are supported:

```text
agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR
agent-librarian validate CATALOG_DIR
agent-librarian report CATALOG_DIR
```

`catalog` also supports the existing documented `--include`, `--exclude`, and
`--strict` arguments. The wrapper rejects unsupported actions and arguments.
It calls the existing Python CLI dispatcher with a fixed argument list. It
does not pass a free-form command string to a shell.

## Proposals

`propose` prints JSON containing:

- the exact command
- expected reads
- expected writes and generated files
- the approval instruction
- the sensitivity class and warning
- source-protection and non-certification notes
- the optional review-summary schema reference

Proposal mode does not run the backend or write generated catalog outputs.
It writes a runtime-state draft only when `--state-out PATH` is explicit.

```powershell
python -m agent_librarian.runtime_wrapper propose catalog examples/sample-collection --out examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose validate examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose report examples/generated-catalog
```

## Approval Behavior

`run` requires `--approve-exact`. The value must match the generated command
string exactly. Approval for one action, path, or optional-argument set does
not authorize another.

```powershell
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "agent-librarian report examples/generated-catalog"
```

An absent or different approval returns a nonzero status without executing
the backend. Shell control characters and command-substitution syntax are
rejected in paths and optional arguments.

## Sensitivity Behavior

The prototype accepts:

```text
synthetic-public
private-local
work-internal
unclear
```

Paths under `examples/` default to `synthetic-public`. Other paths default to
`unclear`.

- `synthetic-public` may run after exact approval.
- `private-local` may run after exact approval and emits a private-output
  warning.
- `work-internal` may be proposed but is blocked from execution by this
  prototype.
- `unclear` may be proposed but is blocked until sensitivity is explicit.

Generated catalog outputs and explicit records inherit source sensitivity.
The wrapper does not publish outputs or certify them as safe to publish.

For a non-example path, set sensitivity explicitly:

```powershell
python -m agent_librarian.runtime_wrapper run validate PRIVATE_CATALOG --sensitivity private-local --approve-exact "agent-librarian validate PRIVATE_CATALOG"
```

## Optional Records

`--records-out DIR` writes these compact JSON files:

```text
runtime-state.json
approval-log.json
execution-record.json
```

No runtime records are written by default. Records contain scope, command,
approval, identifiers, status, and generated file paths. They do not retain
source contents, CLI stdout, CLI stderr, or report text.

Records are explicit user-managed artifacts. Private records remain private
and should not be committed as public examples.

## Summary Handoff

Proposal JSON points to the optional
[review summary schema](../agent/schemas/review-summary.schema.json). This
prototype does not generate a model-authored summary. Any later summary must
remain secondary to deterministic CLI files and command results.

## Non-Goals

The prototype does not add:

- an LLM provider or model call
- network access
- an MCP server, web UI, or background daemon
- arbitrary shell execution or command chaining
- source execution, editing, deletion, or merging
- publication or certification behavior
- durable memory or automatic scan retention
- changes to deterministic CLI output schemas

## Validation

```powershell
python -m pip install -e ".[dev]"
python -m agent_librarian.runtime_wrapper propose catalog examples/sample-collection --out examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose validate examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose report examples/generated-catalog
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "wrong command"
pytest
git diff --check
git diff --exit-code -- examples/generated-catalog
```

The wrong-command example is expected to fail.

## Limitations and Follow-Up

This is a local orchestration prototype, not a complete interaction layer. It
does not interpret natural-language requests, make model-authored summaries,
or define a long-term persistence system.

Related design work:

- [#52 runtime wrapper prototype](https://github.com/ElvinMorales/agent-librarian/issues/52)
- [#54 runtime state and approval logs](https://github.com/ElvinMorales/agent-librarian/issues/54)
- [#55 review summary schema](https://github.com/ElvinMorales/agent-librarian/issues/55)
