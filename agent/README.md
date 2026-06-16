# Agent Layer Design Artifacts

This directory contains design-time artifacts for the planned LLM interaction
layer of `agent-librarian`.

The current project runtime remains the deterministic CLI backend. These files
describe how a future user-facing Artifact Librarian Agent should identify
itself, interact with users, apply safety boundaries, propose bounded CLI
commands, request approval, and summarize generated outputs.

They are not currently loaded as live runtime instructions. A future runtime
wrapper must explicitly implement these contracts and is tracked separately
from this documentation-only design.

The v0.5 portable package workstream treats the files in this directory as the
canonical agent contract. Platform-specific files under `packages/` are
adapters for LLM-native workspaces; they must preserve these source-of-truth
artifacts rather than redefining the agent separately.

## Layer responsibilities

The planned LLM interaction layer is responsible for:

- scoping the user's requested collection and output location
- explaining public/private boundaries before proposing an action
- proposing only documented `agent-librarian` CLI commands
- requesting approval before any future command execution
- summarizing deterministic outputs after the CLI runs
- separating CLI findings from model interpretation
- directing reviewers to generated files as the source of truth

The deterministic CLI backend remains responsible for:

- cataloging selected local artifact collections
- validating generated catalog JSON
- reporting diagnostics, warnings, and overlap candidates
- writing explicit generated outputs for human review

The planned interaction layer is not a catalog engine, shell executor,
autonomous approval system, publication system, or safety certification layer.

## Directory map

- `identity.md`: canonical framework-neutral identity for all future package
  adapters
- `agent.yaml`: layer identity, status, scope, and action surface
- `persona.md`: user-facing identity and communication stance
- `principles.md`: operating rules and source-of-truth boundaries
- `prompts/`: reusable design-time prompt drafts for future runtime work
- `capabilities/`: bounded workflow capability descriptions
- `tools/`: documented CLI action surface for future orchestration
- `workflows/`: approval-gated orchestration patterns for future runtime work
- `policies/`: LLM-layer public-safety, refusal, and redirect policies
- `evals/`: static safety and workflow eval cases for future runtime work
- `governance/`: approval, safety, publication, and refusal boundaries
- `memory/`: durable-memory and retention limits
- `state/`: explicit run-output and future run-state boundaries
- `runtime/`: runtime state and approval-log designs for future wrapper work
- `schemas/`: model-authored output contracts for future interaction-layer summaries

The bounded CLI tool surface is defined in
[agent-librarian-cli.md](tools/agent-librarian-cli.md).

The canonical agent identity is defined in
[identity.md](identity.md).

The catalog-review workflow is defined in
[catalog-review.md](workflows/catalog-review.md).

The LLM-layer public-safety policy is defined in
[public-safety.md](policies/public-safety.md).

The safe-scan eval cases are defined in
[safe-scan-cases.md](evals/safe-scan-cases.md).

Runtime state and approval log artifacts are defined in
[state-and-approval-log.md](runtime/state-and-approval-log.md).

The review summary output contract is defined in
[review-summary.schema.json](schemas/review-summary.schema.json).

The optional local runtime wrapper that prototypes these approval and safety
contracts is documented in
[runtime-wrapper-prototype.md](../docs/runtime-wrapper-prototype.md).

The shared package-adapter foundation is documented in
[portable-agent-packages.md](../docs/portable-agent-packages.md) and
[packages/README.md](../packages/README.md).

## Related design documents

- [Two-Layer Artifact Catalog](../docs/two-layer-artifact-catalog.md)
- [v0.4 Roadmap](../docs/roadmap-v0.4.md)
- [Public Safety](../docs/public-safety.md)
- [Public-Safe Adoption Guide](../docs/adoption-guide.md)
