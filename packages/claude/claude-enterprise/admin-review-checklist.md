# Claude Enterprise Admin Review Checklist

Use this checklist before adapting the Claude package in a private or
work-internal environment.

## Public-Safe Baseline

- Confirm public demos use only `examples/sample-collection`.
- Confirm package examples contain no real private paths, employer-specific
  examples, internal URLs, credentials, secrets, private prompts, private
  traces, logs, memory snapshots, state snapshots, or private generated
  catalogs.
- Confirm users understand that generated outputs inherit source sensitivity.

## Instruction Review

- Managed instructions preserve the canonical `agent/` contract.
- Claude is described as an interface layer.
- Deterministic CLI outputs are named as the source of truth.
- Exact approval is required before local execution.
- Arbitrary shell execution is prohibited.
- Certification claims are prohibited.
- Human review remains required before sharing or publication.

## Tool and Runtime Review

- Approved tool surfaces are documented.
- Runtime-wrapper `propose` is preferred before `run`.
- `run` requires exact approval.
- Private/work-internal execution has a separate authorization and retention
  policy.
- No MCP/API exposure is enabled without separate design review.
- No network behavior is introduced by this package.

## Evidence and Logging Review

- Approval logs are explicit artifacts, not hidden memory.
- Execution records point to the exact approved command.
- Generated outputs and records remain private by default for private source
  material.
- Logs do not embed raw private source contents.
- Saved summaries are secondary review aids and cite deterministic evidence.

