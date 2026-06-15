# Catalog Review Workflow

## Purpose

This document defines the catalog-review workflow for a future LLM
interaction layer. The current project runtime remains the deterministic
`agent-librarian` CLI. This workflow does not add runtime command execution by
itself.

The workflow composes the existing agent identity, operating principles,
prompts, capability description, governance policy, and CLI tool contract into
one approval-gated sequence.

## Workflow status

- **Artifact type:** Workflow / orchestration design
- **Layer:** Planned LLM interaction layer
- **Backend:** Deterministic `agent-librarian` CLI
- **Runtime status:** Design-time only
- **Current enforcement:** Human/process documentation only
- **Future enforcement:** Runtime wrapper or tool adapter, tracked separately

## Layer boundary

The LLM interaction layer scopes the request, explains boundaries, proposes
commands, requests approval, and summarizes outputs. The deterministic CLI
backend performs `catalog`, `validate`, and `report`.

The LLM layer does not catalog files itself, run arbitrary shell commands,
edit source files, approve artifacts, certify safety, or publish generated
outputs.

CLI-generated files and command results remain the source of truth. Model
interpretation is a secondary review aid and must remain distinguishable from
deterministic evidence.

## Workflow overview

```text
1. Receive user request
2. Identify requested action
3. Identify source and output/catalog paths
4. Check sensitivity and public/private boundaries
5. Propose exact documented CLI command
6. Ask for explicit approval
7. Execute only after approval in a future runtime
8. Run validation/report only with approval
9. Summarize deterministic outputs
10. Identify human-review items and safe next steps
```

The sequence is:

```text
user request
  -> scope and safety check
  -> propose exact CLI command
  -> request explicit approval
  -> run deterministic backend
  -> validate/report
  -> summarize generated outputs
  -> identify human-review next steps
```

## Phase 1: Intake and scope

Collect only the information needed to prepare a bounded proposal:

- the user's goal
- requested action: `catalog`, `validate`, `report`, or review generated
  outputs
- explicit source path for `catalog`
- explicit output path for `catalog`
- explicit catalog directory for `validate` or `report`
- whether the material is public, synthetic, personal, work-related,
  client/customer-related, regulated, or otherwise sensitive
- optional `--include`, `--exclude`, or `--strict` arguments

Ask only necessary questions. If the request already provides enough
information to determine the exact documented command, paths, arguments, and
sensitivity boundary, proceed to the command proposal.

Do not use hidden memory, prior runs, or an unspecified folder from earlier
context to fill in missing scope.

## Phase 2: Safety and sensitivity check

Classify the request as one of:

```text
safe synthetic/public example
private local collection
work/client/customer/regulated collection
unclear sensitivity
unsafe publication request
unsupported command or shell request
certification/approval request
private memory/state/log/trace request
```

Apply these behaviors:

- For a safe synthetic/public example, proceed to command proposal.
- For a private local collection, remind the user that generated outputs
  inherit the source collection's sensitivity.
- For work, client, customer, or regulated material, require explicit narrow
  scope and warn that generated outputs must not be published.
- For unclear sensitivity, ask one necessary clarifying question or default
  the material to private.
- For an unsafe publication request, stop and redirect to a safe
  synthetic or private-local pattern.
- For an unsupported command or shell request, stop and point to the
  [CLI tool contract](../tools/agent-librarian-cli.md).
- For a certification or approval request, stop and offer an evidence-based
  summary plus human-review prompts.
- For a private memory, state, log, or trace request, stop public use and
  redirect to a synthetic fixture.

Apply the detailed classifications, refusal cases, and redirect patterns in the
[LLM-layer public-safety policy](../policies/public-safety.md).

## Phase 3: Command proposal

Propose only commands and arguments allowed by the
[CLI tool contract](../tools/agent-librarian-cli.md):

```bash
agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR
agent-librarian validate CATALOG_DIR
agent-librarian report CATALOG_DIR
```

The only allowed optional arguments are for `catalog`:

```text
--include GLOB
--exclude PATTERNS
--strict
```

Every proposal must state:

- the exact command
- the source path or catalog path
- the output path, when applicable
- every optional argument
- what the command will read
- what the command will write
- what will not happen
- the expected generated files, or that no files are generated
- a sensitivity and publication reminder

For `catalog`, the expected generated files are:

```text
index.json
catalog.md
diagnostics.json
overlap-report.json
```

The proposal must explain that source files will be treated as data and will
not be executed, edited, deleted, merged, or published. It must also explain
that `catalog` may create or replace the documented generated files under the
approved output path. `validate` and `report` are read-only against the
approved catalog directory.

## Phase 4: Approval gate

Approval applies only to the exact command and scope shown to the user.

Approval must be explicit. Acceptable examples include:

```text
Approved.
Yes, run that exact command.
Run the command as shown.
```

These responses are not enough for approval:

```text
Sounds good.
Continue.
Do whatever is best.
Just handle it.
Use the same folder as before.
```

A new approval is required when:

- the command changes
- the source path changes
- the output path changes
- the catalog path changes
- optional arguments change
- include or exclude scope changes
- strict mode is added or removed
- the sensitivity classification changes
- the user asks to publish or share generated outputs
- a failed command requires retry with different arguments
- hidden memory or state would otherwise be used to infer prior approval

No execution is authorized if the user refuses, qualifies, or does not provide
approval for the exact proposal.

## Phase 5: Deterministic backend execution

In a future runtime, the wrapper or tool adapter may execute the approved
command only after the approval gate is satisfied. The current documentation
issue does not add execution behavior.

Future execution must:

- run only the approved command
- preserve the approved paths and arguments without broadening scope
- avoid chained commands
- avoid arbitrary shell commands
- avoid editing, deleting, executing, or merging source files
- preserve CLI output
- capture command status for later summary
- keep private output private

Failure does not authorize an automatic retry, changed arguments, broader
scope, shell troubleshooting, or source modification.

## Phase 6: Validation and report

After `catalog` execution, the LLM layer may propose follow-up `validate` and
`report` commands.

Validation and reporting require their own explicit approval unless the user
approved a full sequence in advance with every exact command and path shown.

The recommended sequence is:

```bash
agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR
agent-librarian validate OUTPUT_DIR
agent-librarian report OUTPUT_DIR
```

The LLM layer must explain:

- `validate` checks schema structure only
- `report` summarizes diagnostics, warnings, and overlap candidates
- neither command certifies safety, privacy, correctness, completeness,
  approval, or publication readiness

If validation or reporting fails, preserve and report the failure. Any changed
retry command requires a new proposal and explicit approval.

## Phase 7: Summary and human review

After outputs exist, the LLM layer may summarize:

- the command run
- paths used
- generated files
- validation status
- report summary
- diagnostics
- warning codes
- overlap candidates
- failed or partial parses
- suggested human-review next steps

The summary must distinguish:

```text
deterministic CLI output
model interpretation
human-review recommendation
```

The summary must not:

- invent missing outputs
- contradict CLI output
- hide parse failures
- suppress warnings
- certify safety
- approve publication
- claim artifacts are complete or correct

Human reviewers retain responsibility for correction, consolidation, deletion,
approval, sharing, and publication decisions.

## Approval gates

| Gate | Trigger | Required user confirmation | Notes |
| --- | --- | --- | --- |
| Source-scope gate | Before cataloging a source directory | Exact source path and scan scope | Default unclear sensitivity to private |
| Output-scope gate | Before writing generated files | Exact output path | Catalog may create or replace generated files |
| Optional-argument gate | Before using include/exclude/strict | Exact optional arguments | Scope narrowing/broadening must be visible |
| Validation gate | Before running validate | Exact catalog directory | Schema validation is not safety certification |
| Report gate | Before running report | Exact catalog directory | Report is a review aid, not a decision |
| Retry gate | Before retrying failed command | Exact changed command | No automatic broadening |
| Publication gate | Before sharing outputs | Separate explicit publication review | Private outputs must not be published by default |

Approval for one gate does not imply approval for another gate unless a full
sequence was presented with exact commands, paths, and arguments and explicitly
approved in advance.

## Stop conditions

Stop the workflow if:

- the user asks for arbitrary shell execution
- the user asks to scan private or work material without clear scope
- the user asks to publish private generated outputs
- the user asks the LLM to certify safety, completeness, correctness, or
  approval
- the requested command is not in the CLI tool contract
- the user refuses to approve the exact command
- the proposed command would edit, delete, execute, or merge source files
- the requested scan includes secrets, credentials, regulated data, private
  traces, private prompts, or memory/state snapshots intended for publication

When a safe part of the request remains possible, redirect to a documented
command using synthetic placeholders or a narrowly scoped private-local
pattern.

Detailed stop-condition responses and safe redirects are defined in the
[LLM-layer public-safety policy](../policies/public-safety.md).

## Handoff outputs

The future LLM layer should hand back:

- exact command proposed
- approval status
- command execution status, if applicable
- generated file paths
- validation status
- report summary
- human-review items
- privacy and publication warnings
- next safe command proposal, if needed

This workflow defines the handoff content. The inspectable runtime state,
approval log, command execution record, and summary handoff artifacts are
defined in
[state-and-approval-log.md](../runtime/state-and-approval-log.md).

## Relationship to future runtime work

This workflow informs:

- #49 safety and refusal policy
- #50 safe-scan evaluation cases
- #52 runtime wrapper prototype
- #54 runtime state and approval logs
- #55 review summary schema

This issue does not implement command execution, state logging, provider
integration, an MCP server, a tool adapter, new CLI behavior, or schema
changes.

## Related artifacts

- [Agent Layer Design Artifacts](../README.md)
- [CLI tool contract](../tools/agent-librarian-cli.md)
- [Tool manifest](../tools/tools.yaml)
- [System prompt draft](../prompts/system.md)
- [Catalog directory task prompt](../prompts/tasks/catalog-directory.md)
- [Catalog Collection capability](../capabilities/catalog-collection/SKILL.md)
- [Governance policy](../governance/policy.md)
- [LLM-layer public-safety policy](../policies/public-safety.md)
- [Safe-scan eval cases](../evals/safe-scan-cases.md)
- [State strategy](../state/state-strategy.md)
- [Runtime state and approval log artifacts](../runtime/state-and-approval-log.md)
- [Two-Layer Artifact Catalog](../../docs/two-layer-artifact-catalog.md)
- [v0.4 roadmap](../../docs/roadmap-v0.4.md)
- [Public safety](../../docs/public-safety.md)
