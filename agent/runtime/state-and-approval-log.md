# Runtime State and Approval Log Artifacts

## Purpose

This document defines runtime state and approval log artifacts for a future
LLM interaction layer. The current project runtime remains the deterministic
`agent-librarian` CLI. This document does not add runtime state, command
execution, logging, or persistence by itself.

These artifacts make request scope, command approval, execution evidence, and
summary handoff inspectable without treating model context or conversation
history as authorization.

## Artifact status

- **Artifact type:** Runtime state / approval log design
- **Layer:** Planned LLM interaction layer
- **Backend:** Deterministic `agent-librarian` CLI
- **Runtime status:** Design-time only
- **Current enforcement:** Human/process documentation only
- **Future enforcement:** Runtime wrapper, tool adapter, eval runner, or review
  checks tracked separately

## Layer boundary

The LLM interaction layer may scope a request, propose a documented CLI
command, ask for approval, execute only the approved command in a future
runtime, and summarize generated outputs. The deterministic CLI backend
performs `catalog`, `validate`, and `report`.

The interaction layer does not replace the CLI's cataloging, validation, or
reporting behavior. CLI-generated files and command results remain the source
of truth.

Runtime state and approval logs must be explicit artifacts. Hidden memory,
hidden approval, or hidden state must not change command scope, infer consent,
broaden paths, retry commands, or authorize publication.

## Core distinction: memory, state, approval log, and output

| Concept | Meaning | Persistence | Public-safe? |
| --- | --- | --- | --- |
| Memory | Durable reusable knowledge across sessions | None by default | No private memory in public repo |
| Runtime state | Current run snapshot needed to continue or audit a workflow | Explicit artifact only | Synthetic examples only |
| Approval log | Evidence of exact command/scope approval | Explicit artifact only | Private by default |
| CLI outputs | Generated catalog, diagnostics, overlap, and report artifacts | User-selected output directory | Inherits source sensitivity |
| Summary handoff | Model-authored explanation of generated outputs | Explicit artifact only if saved | Secondary review aid, not source of truth |

Runtime state must not silently become durable memory. Approval evidence is
not reusable authorization, and a summary does not replace deterministic CLI
outputs.

## Runtime state artifact

A runtime state artifact captures the minimum current-run snapshot needed to
continue, inspect, or audit one approval-gated workflow. It should record:

- run id
- created timestamp
- workflow phase
- requested action
- sensitivity class
- source path or catalog path
- output path
- proposed command
- approval status
- execution status
- generated output paths
- validation status
- report status
- warning count
- overlap candidate count
- human-review items
- next proposed action
- privacy boundary
- retention scope

The workflow phase should use a bounded value such as `intake`,
`safety-check`, `proposal`, `approval`, `execution`, `validation`, `report`, or
`summary`. Paths and fields should be present only when applicable to the
requested action.

State must not silently become durable memory. It must not contain raw private
source content, secrets, credentials, internal URLs, real traces, private
prompts, memory snapshots, regulated data, or other private data. State for a
private run remains private even when execution succeeds.

## Approval log artifact

An approval log is evidence that an exact command and its visible scope were
shown to an approver and received a specific result. It should record:

- approval id
- run id
- timestamp
- user approval text or normalized approval status
- exact command shown
- exact source path or catalog path
- exact output path, when applicable
- optional arguments
- expected reads
- expected writes
- expected generated files
- sensitivity class
- privacy warning shown
- approval result: `approved`, `rejected`, `expired`, or `superseded`
- approver role, if applicable, using a generic role label
- reason for reapproval, if any

**Approval applies only to the exact command and scope shown.**

Approval must not be inferred from:

- prior conversation
- prior approval
- remembered paths
- hidden state
- hidden memory
- "continue"
- "sounds good"
- "do whatever is best"

A changed command, path, optional argument, read scope, write scope,
sensitivity class, or expected output requires a new approval record. An
approval log records consent evidence; it does not establish publication
approval or durable authorization for another run.

## Command execution record

A command execution record captures what the deterministic backend actually
did after approval. It should record:

- run id
- approval id
- command executed
- execution timestamp
- exit status
- stdout summary
- stderr summary
- generated files
- diagnostics path
- validation or report status, if applicable
- failure reason, if any
- retry required: yes/no
- reapproval required: yes/no

The execution record must point back to the approval id. The executed command
must match the approved command exactly. A failed execution does not authorize
a broader retry, and any changed command requires new approval.

`validate` and `report` are read-only, but they remain approval-gated because
they read an explicitly selected catalog directory and can expose
sensitive-derived information in command output.

## Summary handoff record

A future LLM layer may hand back an inspectable summary containing:

- command run
- paths used
- generated files
- validation result
- report findings
- diagnostics and warning summary
- overlap candidate summary
- model interpretation, clearly labeled
- human-review recommendations
- privacy and publication reminders
- limitations and a non-certification statement

The summary must not:

- replace CLI outputs
- contradict deterministic outputs
- invent missing outputs
- suppress warnings
- certify safety, privacy, correctness, completeness, approval, or publication
  readiness
- publish private outputs

When saved, a summary handoff is an explicit run artifact that inherits the
run's sensitivity. It is a secondary review aid, not the source of truth.

## Required fields

| Field | Applies to | Required? | Notes |
| --- | --- | --- | --- |
| `run_id` | state, approval, execution, summary | Yes | Stable identifier for one workflow run |
| `approval_id` | approval, execution | Yes for approved execution | Links execution to approval evidence |
| `created_at` / `timestamp` | state, approval, execution | Yes | Use an unambiguous timestamp format |
| `workflow_phase` | state | Yes | Intake, safety-check, proposal, approval, execution, validation, report, summary |
| `requested_action` | state | Yes | Catalog, validate, report, or summarize |
| `sensitivity_class` | state, approval, summary | Yes | Use policy classes |
| `exact_command` | approval, execution | Yes | Must match before execution |
| `source_path` | catalog state/approval | Conditional | Use placeholders in public examples |
| `catalog_dir` | validate/report state/approval | Conditional | Use placeholders in public examples |
| `output_path` | catalog state/approval | Conditional | Catalog writes here |
| `optional_arguments` | state, approval | Conditional | Record every include, exclude, or strict argument |
| `expected_reads` | approval | Yes | Exact approved read scope |
| `expected_writes` | approval | Yes | Empty for read-only actions |
| `expected_generated_files` | approval | Conditional | Required for catalog |
| `privacy_warning_shown` | approval | Yes | Records that sensitivity limits were visible |
| `approval_status` | state, approval | Yes | Pending, approved, rejected, expired, superseded |
| `execution_status` | state, execution | Conditional | Not started, succeeded, failed, skipped |
| `generated_files` | state, execution, summary | Conditional | Explicit output paths |
| `validation_status` | state, execution, summary | Conditional | Report only deterministic results |
| `report_status` | state, execution, summary | Conditional | Report only deterministic results |
| `warning_count` | state, summary | Conditional | Preserve reported warnings |
| `overlap_candidate_count` | state, summary | Conditional | Review prompt, not a decision |
| `human_review_items` | state, summary | Yes when summarizing | Diagnostics, warnings, overlaps, publication concerns |
| `privacy_boundary` | state, summary | Yes | States handling and sharing limits |
| `retention_scope` | state, approval, summary | Yes if saved | States duration, access, and deletion expectations |

## Prohibited fields

Runtime state, approval logs, execution records, summaries, and public
examples must not contain:

- raw source file contents
- secrets
- credentials
- internal URLs
- private local paths in public examples
- employer-specific identifiers
- regulated or private data
- private prompts
- private traces or logs
- memory snapshots
- hidden chain-of-thought
- unsupported shell commands
- inferred approval
- publication approval claims

Records may contain bounded deterministic status summaries, but they must not
embed private source material merely to make a run self-contained.

## Retention and privacy rules

- Private run state is private by default.
- Approval logs inherit source sensitivity.
- Generated outputs inherit source sensitivity.
- Public examples must use synthetic placeholders.
- Do not commit real run state or approval logs from private scans.
- Do not convert private state into durable memory.
- Deletion and retention rules must be explicit in a future runtime.
- A successful run does not make outputs safe to publish.
- Human review is required before sharing.

Any future persistence feature must define purpose, access, duration,
correction, deletion, and review behavior. Retention must be scoped per
artifact and must not be implied by provider history, conversation storage, or
hidden model context.

## Example records

These compact examples are synthetic design fixtures. They do not represent
saved runtime records.

### Runtime state

```json
{
  "run_id": "run_example_001",
  "workflow_phase": "approval",
  "requested_action": "catalog",
  "sensitivity_class": "safe synthetic/public example",
  "source_path": "examples/sample-collection",
  "output_path": "examples/generated-catalog",
  "proposed_command": "agent-librarian catalog examples/sample-collection --out examples/generated-catalog",
  "approval_status": "pending",
  "execution_status": "not_started",
  "privacy_boundary": "public-safe synthetic fixture"
}
```

### Approval log

```json
{
  "approval_id": "approval_example_001",
  "run_id": "run_example_001",
  "approval_status": "approved",
  "exact_command": "agent-librarian catalog examples/sample-collection --out examples/generated-catalog",
  "expected_reads": ["examples/sample-collection"],
  "expected_writes": ["examples/generated-catalog/index.json", "examples/generated-catalog/catalog.md", "examples/generated-catalog/diagnostics.json", "examples/generated-catalog/overlap-report.json"],
  "approval_text": "Approved. Run the command as shown.",
  "scope_note": "Approval applies only to this exact command and scope."
}
```

### Private placeholder

```json
{
  "run_id": "run_private_placeholder",
  "sensitivity_class": "private local collection",
  "source_path": "PRIVATE_SOURCE",
  "output_path": "PRIVATE_OUTPUT",
  "privacy_boundary": "private; do not commit generated outputs or logs"
}
```

Public examples must not replace these placeholders with real user paths,
private collection names, traces, prompts, approvals, or logs.

## Failure and retry handling

- Failed command status must be recorded.
- Partial generated outputs must be listed if present.
- Parse warnings must not be suppressed.
- Retrying with changed arguments requires new approval.
- Broader scope after failure requires new approval.
- Failure does not authorize shell troubleshooting.
- Failure does not authorize source edits, deletes, or merges.
- Missing outputs must not be invented.
- The summary must clearly label failure and incomplete outputs.

The execution record should retain the original approval link and identify
whether the same exact command is eligible for a separately approved retry.
Any changed command must create a new approval record rather than mutate the
prior approval evidence.

## Relationship to future runtime work

This document informs:

- #52 runtime wrapper prototype
- #55 review summary schema

It consumes:

- #47 CLI tool contract
- #48 catalog-review workflow
- #49 public-safety policy
- #50 safe-scan eval cases

Issue #54 does not implement runtime state persistence, command execution,
provider integration, an MCP server, a tool adapter, an eval runner, or a
review summary schema. Those capabilities require separately scoped runtime
or schema work.

## Related artifacts

- [Agent Layer Design Artifacts](../README.md)
- [System prompt draft](../prompts/system.md)
- [CLI tool contract](../tools/agent-librarian-cli.md)
- [Catalog Review Workflow](../workflows/catalog-review.md)
- [LLM-Layer Public Safety Policy](../policies/public-safety.md)
- [Safe-scan eval cases](../evals/safe-scan-cases.md)
- [Memory policy](../memory/policy.md)
- [State strategy](../state/state-strategy.md)
- [Two-Layer Artifact Catalog](../../docs/two-layer-artifact-catalog.md)
- [v0.4 roadmap](../../docs/roadmap-v0.4.md)
