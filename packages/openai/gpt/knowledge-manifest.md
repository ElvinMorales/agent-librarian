# GPT Knowledge Manifest

Use public-safe source-of-truth files for an advisory GPT. Upload only files
needed for review.

## Recommended Reference Files

```text
README.md
agent/identity.md
agent/tools/agent-librarian-cli.md
agent/workflows/catalog-review.md
agent/policies/public-safety.md
agent/evals/safe-scan-cases.md
agent/runtime/state-and-approval-log.md
agent/schemas/review-summary.schema.json
docs/runtime-wrapper-prototype.md
docs/portable-agent-packages.md
packages/shared/conformance/scenarios.md
examples/generated-catalog/catalog.md
examples/generated-catalog/diagnostics.json
examples/generated-catalog/overlap-report.json
```

## Optional Context

```text
packages/openai/gpt/instructions.md
packages/openai/gpt/conversation-starters.md
docs/demos/gpt-chat-end-to-end.md
```

## Do Not Upload

Do not upload private scans, private generated outputs, work folders, secrets,
credentials, private journals, private prompts, private traces, memory
snapshots, state snapshots, approval logs, runtime records, employer/client
data, customer data, regulated data, internal URLs, or any material that has
not been separately reviewed for sharing.

Generated outputs inherit source sensitivity. Private-derived catalogs,
reports, summaries, traces, and state files remain private by default.

