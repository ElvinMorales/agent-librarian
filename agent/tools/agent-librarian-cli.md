# agent-librarian CLI Tool Contract

## Purpose

This document defines the bounded CLI tool contract for a future LLM
interaction layer. The current project runtime remains the deterministic
`agent-librarian` CLI. This contract does not add runtime command execution by
itself.

## Contract status

- **Artifact type:** Tool contract
- **Layer:** Planned LLM interaction layer calling deterministic CLI backend
- **Runtime status:** Design-time only
- **Current enforcement:** Human/process documentation only
- **Future enforcement:** Runtime wrapper or tool adapter, tracked separately

## Layer boundary

The LLM interaction layer may scope requests, explain boundaries, propose
commands, ask for approval, and summarize outputs. The deterministic CLI
backend performs the actual catalog, validate, and report operations.

The interaction layer is not a shell, catalog engine, source editor,
publication system, approval authority, or certification layer. The backend
remains directly usable without an LLM.

## Approved commands

The future LLM interaction layer may propose only these deterministic CLI
actions:

```text
agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR
agent-librarian validate CATALOG_DIR
agent-librarian report CATALOG_DIR
```

The only optional arguments in this contract are `--include GLOB`,
`--exclude PATTERNS`, and `--strict` for `catalog`. No other CLI actions,
arguments, shell commands, or local file operations are approved.

## Command: catalog

### Purpose

Scan a selected local artifact collection as data and write the documented
generated catalog outputs for human review.

### Allowed form

```bash
agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR
agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR --include GLOB
agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR --exclude PATTERNS
agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR --strict
```

The documented optional arguments may be combined or repeated only as
supported by CLI help. They must remain visible in the exact command presented
for approval.

### Required inputs

- `SOURCE_DIR`: explicit directory containing the approved source collection
- `OUTPUT_DIR`: explicit directory where generated files may be written

### Optional arguments

- `--include GLOB`: narrow inventory scope to matching files; may be repeated
- `--exclude PATTERNS`: add comma-separated path or name patterns to the safe
  default excludes; may be repeated
- `--strict`: exit non-zero if a selected file fails to parse

### Reads

The command reads supported files under `SOURCE_DIR` that match the approved
include and exclude scope. Selected files are treated as data and are not
executed.

### Writes

The command writes generated files under `OUTPUT_DIR` only:

```text
index.json
catalog.md
diagnostics.json
overlap-report.json
```

### Side effects

The command may create `OUTPUT_DIR` and may create or replace the documented
generated outputs in that directory. It must not edit, delete, execute, merge,
or publish source artifacts.

### Expected outputs

The expected results are the four generated files and CLI status output
identifying the output directory and written filenames. Strict mode may still
write outputs before returning a non-zero status for failed parses.

### Approval requirement

Explicit approval is required before execution in any future LLM runtime. The
approval request must show the exact `SOURCE_DIR`, `OUTPUT_DIR`, optional
arguments, expected read scope, expected write scope, and generated files.

### Safety notes

Generated files can expose source names, relative paths, metadata,
diagnostics, warnings, and overlap candidates. Local deterministic execution
does not make the source or outputs safe to publish.

### What the LLM layer may summarize

After execution, the LLM layer may summarize the actual command status,
generated filenames, deterministic entry or diagnostic counts, parse
statuses, warnings, and overlap candidates present in CLI results.

### What the LLM layer must not claim

The LLM layer must not claim that the catalog is complete, semantically
correct, private, safe, approved, or ready to publish. It must not claim that
source artifacts were changed, consolidated, or reviewed beyond the evidence
in the CLI outputs.

## Command: validate

### Purpose

Check the generated catalog JSON files in an existing catalog directory
against the bundled schemas.

### Allowed form

```bash
agent-librarian validate CATALOG_DIR
```

### Required inputs

- `CATALOG_DIR`: explicit directory containing generated catalog JSON files

### Optional arguments

None.

### Reads

The command reads generated catalog JSON files under `CATALOG_DIR`. It does
not rescan the source collection.

### Writes

None.

### Side effects

None. Validation is read-only against the existing generated catalog.

### Expected outputs

The command reports per-file schema validation results and an overall pass or
failure status.

### Approval requirement

Explicit approval is required before execution in any future LLM runtime. The
approval request must show the exact `CATALOG_DIR` and expected read scope.

### Safety notes

Validation reports schema validity only. It does not certify safety, privacy,
completeness, semantic correctness, approval, or publication readiness.

### What the LLM layer may summarize

The LLM layer may summarize the actual per-file pass or failure results,
reported validation messages, and overall command status.

### What the LLM layer must not claim

The LLM layer must not describe successful schema validation as proof that the
source collection or generated catalog is safe, private, complete, correct,
approved, or ready to publish.

## Command: report

### Purpose

Read an existing generated catalog and produce a human-readable review
summary.

### Allowed form

```bash
agent-librarian report CATALOG_DIR
```

### Required inputs

- `CATALOG_DIR`: explicit directory containing generated catalog files

### Optional arguments

None.

### Reads

The command reads generated catalog files under `CATALOG_DIR`. It does not
rescan the source collection.

### Writes

None. The human-readable review summary is emitted as command output.

### Side effects

None. Reporting is read-only against the existing generated catalog and does
not approve, merge, delete, publish, or certify artifacts.

### Expected outputs

The command produces a human-readable summary of diagnostics, warnings, and
overlap candidates for review.

### Approval requirement

Explicit approval is required before execution in any future LLM runtime. The
approval request must show the exact `CATALOG_DIR` and expected read scope.

### Safety notes

Warnings and overlap candidates are review prompts, not decisions. Report
output can contain information derived from a private source collection and
must remain private with that collection.

### What the LLM layer may summarize

The LLM layer may summarize the report sections, deterministic counts,
warnings, overlap candidates, and stated human-review prompts that the command
actually produced.

### What the LLM layer must not claim

The LLM layer must not treat the report as an artifact approval, merge,
deletion, publication, safety, privacy, completeness, or correctness
decision.

## Approval requirements

A future LLM runtime must obtain explicit approval before executing any
command. Approval applies only to the exact command and scope shown to the
user.

The approval request must show:

- the exact command
- the source path or catalog path
- the output path, when applicable
- every optional argument
- expected reads
- expected writes
- expected generated files
- a privacy and sensitivity reminder

Approval must not be inferred from:

- broad user intent
- prior approval
- prior conversation
- hidden memory
- hidden state
- a request to "just do it"
- a request to publish private outputs

Changed paths, arguments, read scope, write scope, or command action require a
new approval request.

## Input and output rules

- Use explicit paths in every proposed command and approval request.
- Use generic placeholders and public-safe synthetic examples in repository
  documentation.
- Treat private, work, client, customer, personal, and regulated collections
  as private by default.
- Do not commit generated catalogs from private collections.
- Do not convert private scan results into public examples, prompt context, or
  model-authored summaries for publication.
- Do not include secrets, credentials, internal URLs, private traces, private
  prompts, or memory or state snapshots in public inputs, outputs, examples,
  or logs.
- Keep CLI output and any model summary within the approved collection's
  privacy boundary.

## Prohibited actions

The future LLM interaction layer and any implementing adapter must not:

- run arbitrary shell commands
- execute source files
- edit source files
- delete source files
- merge or consolidate source files
- publish private generated outputs
- scan private or work folders without explicit scoped approval
- expand command, read, or write scope after approval
- run commands not listed in this contract
- claim validation is safety certification
- claim reports are approval decisions
- perform model-generated cataloging without CLI evidence
- use hidden memory or hidden runtime state to change tool scope
- rewrite, move, publish, or otherwise manage source artifacts through this
  contract

## Error handling

When a command fails, the future LLM layer must:

- not invent missing results
- summarize the reported error without suppressing relevant details
- identify the exact failed command
- point to available diagnostics or partial generated outputs
- suggest bounded, safe next steps
- ask for explicit approval before retrying with changed arguments
- avoid automatically broadening source, catalog, or output scope
- preserve and report parse warnings and diagnostics

A failed command does not authorize a different command, changed arguments, a
broader scan, arbitrary shell troubleshooting, or source modification.

## Source-of-truth rule

CLI-generated files and command outputs remain the source of truth. Model
summaries are secondary review aids and must not replace, contradict, or
fabricate deterministic CLI outputs.

## Public/private safety rules

- Public examples must use synthetic collections and generic paths.
- Private, employer, client, customer, personal, and regulated collections
  remain private by default.
- Generated catalogs and reports inherit the sensitivity of their source
  collection.
- A local scan or successful validation does not make an artifact public-safe.
- Human review is required before sharing or publishing any generated output.
- The interaction layer must not expose private inputs or outputs, imply
  employer endorsement, or certify publication readiness.

## Relationship to future runtime work

This contract informs:

- #48 catalog-review workflow and approval gates
- #49 safety and refusal policy
- #50 public-safe evaluation cases
- #52 optional runtime wrapper prototype
- #54 runtime state and approval logs
- #55 review summary schema

Issue #47 does not implement command execution, a runtime wrapper, provider
integration, an MCP server, a tool adapter, or new CLI behavior. A future
runtime must explicitly enforce this contract and remain bounded to the
deterministic backend.

## Related artifacts

- [Agent Layer Design Artifacts](../README.md)
- [Tool manifest](tools.yaml)
- [System prompt draft](../prompts/system.md)
- [Catalog directory task](../prompts/tasks/catalog-directory.md)
- [Catalog Collection capability](../capabilities/catalog-collection/SKILL.md)
- [Governance policy](../governance/policy.md)
- [Operating principles](../principles.md)
- [State strategy](../state/state-strategy.md)
- [Two-Layer Artifact Catalog](../../docs/two-layer-artifact-catalog.md)
- [v0.4 roadmap](../../docs/roadmap-v0.4.md)
- [Public safety](../../docs/public-safety.md)
- [Public-Safe Adoption Guide](../../docs/adoption-guide.md)
