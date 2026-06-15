# v0.4 Roadmap - LLM Layer and Feedback

## Purpose

This roadmap organizes the next project phase around a bounded LLM interaction
layer, the existing deterministic CLI backend, and public-safe feedback from
the Agentic AI forum. It describes direction and sequencing; it does not make
every listed item a release commitment.

## Release theme

The v0.4 theme is **bounded LLM orchestration over deterministic artifact
operations**.

`agent-librarian` is evolving toward a two-layer agentic architecture:

1. **LLM interaction layer** - scopes user intent, explains safety boundaries,
   proposes bounded commands, asks for approval before execution, and
   summarizes generated outputs.
2. **Deterministic CLI backend** - performs `catalog`, `validate`, and `report`
   actions against local artifact collections.

The LLM layer should orchestrate the workflow, not invent catalog results.
CLI-generated files remain the source of truth for review.

## Current baseline

Version 0.3.0 already includes:

- a deterministic local CLI
- catalog generation
- schema validation
- a read-only `report` command
- a showcase brief
- a demo walkthrough
- a forum demo runbook
- a taxonomy-aligned architecture map
- a public-safe adoption guide
- warning-code documentation and a synchronization check
- release hygiene

The current v0.3 runtime does not call an LLM, execute scanned artifacts,
maintain hidden memory or session state, or make artifact-management
decisions.

## Target architecture

```text
user
  -> LLM interaction layer
       -> scope intent and selected collection
       -> explain public/private safety boundaries
       -> propose a bounded, documented CLI command
       -> ask for human approval before execution
       -> invoke the deterministic backend
       -> summarize generated outputs with source references
  -> deterministic CLI backend
       -> catalog
       -> validate
       -> report
       -> explicit generated files for human review
```

The interaction layer should use a defined tool contract and visible approval
gates. It should not substitute model claims for generated catalog evidence.
It should not run arbitrary shell commands or certify artifacts as safe,
complete, approved, or ready to publish. The backend should remain usable
directly without an LLM.

## Planned work

| Issue | Theme | Purpose | Runtime impact |
| --- | --- | --- | --- |
| #45 | Documentation adaptation | Adapt docs for LLM interaction layer + deterministic CLI backend | Docs only |
| #46 | Agent identity | Define LLM Artifact Librarian identity and operating-style design artifacts under `agent/` | Docs only |
| #47 | Tool contract | Define the bounded [`agent-librarian` CLI tool contract](../agent/tools/agent-librarian-cli.md) for the LLM layer | Docs only |
| #48 | Workflow | Define the [catalog-review workflow and approval gates](../agent/workflows/catalog-review.md) | Docs only |
| #49 | Safety policy | Define [refusal and approval-required cases](../agent/policies/public-safety.md) | Docs only |
| #50 | Evals | Add safe-scan cases for future LLM layer | Static eval artifacts |
| #51 | Roadmap/feedback | Add feedback log and v0.4 roadmap | Docs only |
| #52 | Runtime prototype | Prototype optional local LLM orchestration wrapper | Future runtime |
| #53 | Taxonomy catalog | Classify two-layer architecture across taxonomy buckets | Docs only |
| #54 | Runtime state | Define run-state and approval-log artifacts | Design/schema docs |
| #55 | Summary schema | Draft LLM review summary output contract | Schema/design |

The [Two-Layer Artifact Catalog](two-layer-artifact-catalog.md) classifies the
planned LLM interaction layer and current deterministic CLI backend across the
14 taxonomy buckets.

## Suggested implementation order

1. #51 - Roadmap and feedback log
2. #45 - Documentation adaptation for LLM layer + CLI backend
3. #53 - Two-layer taxonomy artifact catalog
4. #46 - LLM identity and operating style
5. #47 - CLI tool contract
6. #48 - Workflow and approval gates
7. #49 - Safety policy and refusal cases
8. #54 - Runtime state and approval-log artifacts
9. #55 - LLM review summary output contract
10. #50 - Safe-scan eval cases
11. #52 - Runtime wrapper prototype

This order establishes the public framing, contracts, safety boundaries, and
inspectable artifacts before adding optional runtime orchestration.

The identity and operating-style design artifacts for #46 are organized under
[`agent/`](../agent/README.md). They describe future interaction-layer
behavior and are not loaded by the current CLI runtime.

The design-time tool contract for #47 is documented in
[`agent/tools/agent-librarian-cli.md`](../agent/tools/agent-librarian-cli.md).
It limits future orchestration to approval-gated `catalog`, `validate`, and
`report` commands and does not implement runtime execution.

The design-time workflow for #48 is documented in
[`agent/workflows/catalog-review.md`](../agent/workflows/catalog-review.md).
It defines intake, safety classification, exact-command approval, backend
execution boundaries, validation and reporting gates, and human-review handoff
without adding runtime execution.

The design-time safety policy for #49 is documented in
[`agent/policies/public-safety.md`](../agent/policies/public-safety.md). It
defines sensitivity classes, approval-required cases, refusal and redirect
patterns, publication boundaries, claims limits, memory and state safety, and
error handling without adding runtime enforcement.

## Out of scope for v0.4

- no autonomous artifact approval
- no safety certification
- no publishing private generated catalogs
- no scanning private or work folders in public demos
- no arbitrary shell execution
- no hidden memory store
- no hidden runtime state
- no provider lock-in unless explicitly chosen later
- no PyPI or package publishing unless separately scoped
- no schema-breaking changes unless justified

## Public-safety boundaries

- Public examples and demos must use synthetic repository fixtures.
- The LLM layer must not weaken CLI scan-scope or output-review boundaries.
- Private prompts, logs, traces, memory or state snapshots, credentials,
  secrets, regulated data, employer workflows, internal URLs, and proprietary
  examples must not enter public artifacts.
- Proposed commands must show the selected input and output scope before
  execution.
- Generated catalogs require human review before sharing or publication.
- Model summaries must distinguish deterministic CLI findings from model
  interpretation.
- The project must not imply employer sponsorship, approval, or endorsement.

## Success criteria

v0.4 succeeds if the project has a clear, public-safe LLM-layer design that
preserves the deterministic CLI as the backend source of truth.

Supporting indicators:

- the LLM identity, tool contract, workflow, and safety policy are explicit
- approval-required and refusal cases are documented
- run state and summary outputs have inspectable contracts
- safe-scan eval cases cover important public/private boundaries
- any runtime prototype is optional and cannot bypass the deterministic CLI
- forum feedback can be retained without automatically becoming roadmap work

## Related issues

- #45 - Documentation adaptation
- #46 - Agent identity
- #47 - Tool contract
- #48 - Workflow and approval gates
- #49 - [Safety policy](../agent/policies/public-safety.md)
- #50 - Safe-scan evals
- #51 - Roadmap and feedback log
- #52 - Runtime prototype
- #53 - Taxonomy catalog
- #54 - Runtime state and approval log
- #55 - Review summary schema

## Related docs

- [Forum feedback log](forum-feedback-log.md)
- [Project overview](../README.md)
- [Showcase brief](showcase-brief.md)
- [Demo walkthrough](demo-walkthrough.md)
- [Forum demo runbook](forum-demo-runbook.md)
- [Taxonomy-aligned architecture map](taxonomy-architecture-map.md)
- [Two-Layer Artifact Catalog](two-layer-artifact-catalog.md)
- [Agent Layer Design Artifacts](../agent/README.md)
- [LLM-Layer Public Safety Policy](../agent/policies/public-safety.md)
- [Public-safe adoption guide](adoption-guide.md)
- [Public safety](public-safety.md)
