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

The bounded CLI tool surface is defined in
[agent-librarian-cli.md](tools/agent-librarian-cli.md).

The catalog-review workflow is defined in
[catalog-review.md](workflows/catalog-review.md).

The LLM-layer public-safety policy is defined in
[public-safety.md](policies/public-safety.md).

The safe-scan eval cases are defined in
[safe-scan-cases.md](evals/safe-scan-cases.md).

## Related design documents

- [Two-Layer Artifact Catalog](../docs/two-layer-artifact-catalog.md)
- [v0.4 Roadmap](../docs/roadmap-v0.4.md)
- [Public Safety](../docs/public-safety.md)
- [Public-Safe Adoption Guide](../docs/adoption-guide.md)
