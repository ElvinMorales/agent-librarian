# Taxonomy Alignment

`agent-librarian` uses the stable framework-neutral 14-bucket model from the
Agentic AI Artifact Taxonomy as its internal classification vocabulary.

| Bucket | Cataloging examples |
| --- | --- |
| Identity | Agent manifests, roles, purpose, ownership |
| Operating style | Principles, collaboration and behavior guidance |
| Capability modules | Skills and reusable procedures |
| Tools | Callable tool definitions and permission surfaces |
| Knowledge and resources | References, datasets, and resource catalogs |
| Prompts and interfaces | System prompts, task templates, input contracts |
| Memory | Durable-memory policies and schemas |
| State | Run-state strategies and checkpoint schemas |
| Planning and orchestration | Plans, routers, workflows, and handoffs |
| Guardrails and governance | Safety, approval, and review policies |
| Outputs and schemas | Output contracts, schemas, and report formats |
| Evaluation and observability | Evals, rubrics, metrics, and trace schemas |
| Runtime and deployment | Packaging, environment, and protocol adapters |
| Learning and iteration | Changelogs, feedback, and release notes |

## Boundaries

- Generic artifact classes are assigned before framework or protocol hints.
- MCP, A2A, Claude, OpenAI, Codex, and orchestration framework surfaces are
  optional mappings, not taxonomy buckets.
- Memory is durable knowledge for later reuse. State is an execution snapshot
  for continuation, replay, or inspection.
- Design-time definitions, runtime records, and iteration artifacts remain
  distinct. Public collections should generally contain design-time artifacts
  and synthetic iteration fixtures, not real runtime records.

The MVP recognizes a focused subset of filenames and otherwise emits
`unknown_artifact_type` for human classification.
