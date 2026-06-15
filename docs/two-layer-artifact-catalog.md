# Two-Layer Artifact Catalog

## Purpose

This document catalogs the artifacts for the planned two-layer
`agent-librarian` architecture:

1. **LLM interaction layer** - user-facing identity, scoping, safety
   explanation, command proposal, approval, and summary.
2. **Deterministic CLI backend** - local `catalog`, `validate`, and `report`
   actions against selected artifact collections.

`agent-librarian` currently provides a deterministic CLI backend for
cataloging, validating, and reviewing local agentic AI artifact collections.
The v0.4 direction adds a planned LLM interaction layer in front of that
backend.

The LLM layer should orchestrate the workflow, not replace deterministic
cataloging logic or invent catalog results. CLI-generated files remain the
source of truth for review.

This catalog makes the v0.4 direction inspectable before runtime work begins.
It does not claim that the planned LLM layer is part of current v0.3 runtime
behavior.

## Architecture summary

```text
user
  -> planned LLM interaction layer
       -> identify its role and limits
       -> scope the selected collection and output location
       -> explain public/private safety boundaries
       -> propose a bounded, documented CLI command
       -> request human approval before execution
       -> invoke the deterministic CLI backend
       -> summarize generated outputs with source references
  -> current deterministic CLI backend
       -> catalog
       -> validate
       -> report
       -> explicit generated files for human review
```

The backend remains directly usable without an LLM. The future interaction
layer must use documented command contracts, cannot run arbitrary shell
commands, and cannot bypass approval or scan-scope boundaries.

Validation and reporting are review aids, not safety certification. A future
LLM summary must not claim that artifacts are safe, complete, approved, or
ready to publish.

## How to read this catalog

The table separates artifacts that exist today from artifacts proposed for the
LLM interaction layer. Current entries include executable backend surfaces,
generated outputs, and design-time documents that describe the deterministic
system. Files under `agent/` are not loaded as runtime LLM instructions.

Planned paths are directional names for later issues, not files created or
runtime behavior implemented by this documentation issue. Public/private
notes apply to source collections, generated outputs, future run records, and
model-authored summaries.

## Artifact catalog

| Taxonomy bucket | Artifact class | Current CLI/backend artifacts | Planned LLM-layer artifacts | Role in the system | Public/private boundary note |
| --- | --- | --- | --- | --- | --- |
| 1. Identity | Project and agent identity | `README.md`, `docs/showcase-brief.md`, `agent/agent.yaml`, `agent/persona.md`, package name `agent-librarian` | LLM Artifact Librarian identity, interaction-layer README, and future system identity instructions from #46 | Defines what the system is, which layer is active, and the limits of each layer | Do not claim current autonomous or LLM-powered runtime behavior; do not imply employer endorsement |
| 2. Operating style | Operating rules and interaction principles | `agent/principles.md`, `agent/persona.md`, CLI help, and docs describing deterministic, local, human-review-first behavior | Interaction rules for uncertainty, safety explanations, command proposals, approvals, and evidence-based summaries from #46 | Defines how each layer behaves and communicates limits | The future layer must preserve local-only, private-by-default, and human-review boundaries |
| 3. Capability modules | Bounded capability descriptions | `agent/capabilities/catalog-collection/SKILL.md` and the implemented `catalog`, `validate`, and `report` commands | Bounded catalog-review capability or workflow documentation that composes only documented backend actions | Describes what the system can perform and where each capability is implemented | The LLM layer may propose supported actions but must not invent commands or imply unsupported capabilities |
| 4. Tools | Tool interfaces and contracts | `src/agent_librarian/cli.py`, `agent/tools/tools.yaml`, command help, scanner/parser modules, validation, and read-only reporting | A bounded CLI tool contract from #47, such as `agent/tools/agent-librarian-cli.md` | Defines the allowed command surface, arguments, outputs, permissions, and side effects | No arbitrary shell execution; selected input and output scope must be visible before approval |
| 5. Knowledge/resources | Reference material, schemas, and sample collections | `docs/`, `examples/sample-collection/`, `examples/generated-catalog/`, `schemas/`, and packaged schema resources | Public-safe grounding material, synthetic review examples, and references to backend contracts | Provides context for explanations, command selection, and review | Public examples must remain synthetic; private collection content must not become shared grounding material |
| 6. Prompts/interfaces | User and system interaction surfaces | CLI arguments and help, include/exclude patterns, README examples, `agent/prompts/system.md`, and `agent/prompts/tasks/catalog-directory.md` as design-time descriptions | Future interaction-layer system prompt, user request templates, approval prompt, and summary prompt | Defines how users request work and how the interaction layer proposes and explains actions | Prompts must not embed private paths, secrets, employer workflows, private scans, or internal examples |
| 7. Memory | Durable reusable knowledge and retention policy | `agent/memory/policy.md`; no durable memory exists in the CLI runtime | A memory policy documenting no durable memory by default and any later consent, retention, correction, and deletion rules | Defines what, if anything, may be reused across sessions | Private scans, generated catalogs, approvals, and summaries must not silently become durable memory |
| 8. State | Explicit run, session, and approval records | `agent/state/state-strategy.md`; generated `index.json`, `diagnostics.json`, `overlap-report.json`, and `catalog.md` expose run results without hidden session state | Explicit run-state and approval-log artifacts from #54, potentially with inspectable schemas | Captures selected scope, proposed action, approval evidence, execution result, and generated review artifacts | State from private scans is private by default and must not be committed as a public example |
| 9. Planning/orchestration | Workflow sequence and approval flow | `docs/demo-walkthrough.md`, `docs/forum-demo-runbook.md`, `docs/developer-workflow.md`, and the documented `catalog` -> `validate` -> `report` sequence | Catalog-review workflow and approval gates from #48 | Orders scoping, command proposal, approval, backend execution, validation, reporting, and summary | Human approval is required before future LLM-triggered execution; approval must not be inferred from conversation |
| 10. Guardrails/governance | Safety policies, refusals, and review constraints | `docs/public-safety.md`, `docs/adoption-guide.md`, `agent/governance/policy.md`, README non-goals, and warning guidance | Interaction-layer safety policy and refusal/approval-required cases from #49 | Prevents unsafe scanning, disclosure, unsupported execution, certification claims, and boundary violations | The LLM layer must not weaken existing scan, publication, privacy, or human-review boundaries |
| 11. Outputs/schemas | Output contracts and review artifacts | `schemas/`, packaged schemas, `index.json`, `diagnostics.json`, `overlap-report.json`, `catalog.md`, and CLI report text | Review-summary contract from #55, with references back to CLI-generated evidence | Makes deterministic findings and model-authored interpretation inspectable and reviewable | LLM summaries are secondary artifacts; CLI outputs remain the source of truth and must be reviewed before sharing |
| 12. Evaluation/observability | Tests, diagnostics, validation, reports, and evals | `tests/`, GitHub Actions CI, `diagnostics.json`, `validate`, `report`, and the warning-reference synchronization test | Public-safe scan cases from #50 and future mock LLM evals for scoping, refusal, approval, and summary behavior | Checks deterministic behavior, warning contracts, safety expectations, and future orchestration behavior | Evals must use synthetic, public-safe inputs and must not include real traces, prompts, logs, or user data |
| 13. Runtime/deployment | Execution environment, packaging, and adapters | `pyproject.toml`, local CLI entry point, supported Python versions, GitHub Actions CI, and release tags | Optional local runtime wrapper and provider/mock adapter documentation from #52 | Defines how the backend runs today and how an optional interaction layer may invoke it later | The wrapper must remain optional, cannot bypass the CLI, and must not require public exposure of private collections |
| 14. Learning/iteration | Feedback, decisions, backlog, and release iteration | `CHANGELOG.md`, GitHub issues and pull requests, `docs/release-checklist.md`, `docs/forum-feedback-log.md`, and `docs/roadmap-v0.4.md` | Public-safe decision records and follow-up issues informed by evals and feedback | Converts reviewed observations into explicitly scoped, versioned work | Feedback must be generic and public-safe before entering the repo; the runtime must not learn from users automatically |

## Boundary notes

### Memory vs state

Memory is durable knowledge reused across sessions. State is an execution
snapshot or run record. The current CLI does not maintain hidden memory or
hidden runtime state. Future runtime state, approval logs, and summaries should
be explicit artifacts, especially for private scans.

Generated files persist because the user explicitly writes them to an output
directory. They are review artifacts, not a hidden memory store or resumable
conversation state.

### Design-time vs runtime

Design-time artifacts include identity files, operating rules, tool contracts,
prompts, policies, schemas, workflows, and docs. Runtime artifacts include
generated catalogs, diagnostics, overlap reports, run state, approval logs,
and review summaries.

The current `agent/` files describe the deterministic system at design time;
the CLI does not load them as runtime instructions. Future LLM design files
would remain design-time artifacts until an explicitly scoped runtime wrapper
uses them.

### Source of truth

The deterministic CLI backend remains the source of truth for catalog
generation, validation, and reports. A future LLM layer may summarize and
guide review, but it must not replace the generated output files or certify
them as safe.

Model-authored summaries should cite or point reviewers to the relevant
generated files and clearly distinguish deterministic findings from model
interpretation.

## Relationship to future runtime work

This documentation-only catalog establishes classifications and boundaries for
later issues. It does not add an LLM runtime, provider integration, command
execution wrapper, memory store, runtime state, approval log, or summary
schema.

The catalog informs:

- #46 - agent identity and operating style
- #47 - bounded CLI tool contract
- #48 - catalog-review workflow and approval gates
- #49 - safety policy and refusal cases
- #50 - public-safe scan evals
- #52 - optional runtime wrapper prototype
- #54 - explicit runtime state and approval logs
- #55 - review summary schema

Those issues should preserve the separation between model orchestration and
deterministic evidence established here. Runtime work should begin only after
the relevant identity, tool, workflow, safety, state, and output contracts are
inspectable.

## Related docs

- [v0.4 roadmap](roadmap-v0.4.md)
- [Taxonomy-aligned architecture map](taxonomy-architecture-map.md)
- [Showcase brief](showcase-brief.md)
- [Demo walkthrough](demo-walkthrough.md)
- [Forum demo runbook](forum-demo-runbook.md)
- [Public-safe adoption guide](adoption-guide.md)
- [Public safety](public-safety.md)
