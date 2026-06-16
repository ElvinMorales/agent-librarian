# GPT and ChatGPT Project End-to-End Advisory Demo

This guide shows the advisory OpenAI chat path:

```text
User uploads or pastes public-safe generated outputs
-> GPT or ChatGPT Project explains the Agent Librarian workflow
-> chat reviews deterministic evidence
-> chat asks the user to run local commands when evidence is missing
-> human reviews generated outputs and publication risk
```

Regular GPT chats and ChatGPT Projects do not run the local CLI by default.
They are advisory unless a future reviewed Action/API wrapper exists.

## Setup

Use either:

```text
packages/openai/gpt/instructions.md
packages/openai/gpt/knowledge-manifest.md
packages/openai/gpt/conversation-starters.md
```

or:

```text
packages/openai/chatgpt-project/project-instructions.md
packages/openai/chatgpt-project/source-files-to-upload.md
packages/openai/chatgpt-project/demo-thread-prompt.md
```

Upload or paste only public-safe files listed in the manifest, such as:

```text
README.md
agent/identity.md
agent/tools/agent-librarian-cli.md
agent/workflows/catalog-review.md
agent/policies/public-safety.md
packages/shared/conformance/scenarios.md
examples/generated-catalog/catalog.md
examples/generated-catalog/diagnostics.json
examples/generated-catalog/overlap-report.json
```

## Local Evidence Commands

If validation or report evidence is missing, the chat should ask the user to
run deterministic commands locally:

```bash
agent-librarian validate examples/generated-catalog
agent-librarian report examples/generated-catalog
```

The chat must not claim it ran those commands. It may review pasted command
output after the user supplies it.

## Demo Thread

Use this prompt:

```text
Explain Agent Librarian in plain language using the uploaded files. Review the
uploaded generated catalog outputs. State clearly that this chat is advisory
and does not run the local CLI by default. If evidence is missing, ask me to
run the exact local commands. Do not certify safety or publication readiness.
```

## What This Proves

This path proves the same Agent Librarian contract can be used in advisory
OpenAI chat workspaces. The chat can explain the workflow, review uploaded
deterministic evidence, and guide next steps without inventing execution.

## What This Does Not Prove

This does not prove local command execution, autonomous scanning, private-data
safety, semantic correctness, completeness, compliance, approval, or
publication readiness. Future Actions/API wrappers are out of scope for this
package.

## Safety Warnings

Do not upload private scans, private generated outputs, work folders, secrets,
credentials, private journals, private prompts, private traces, memory
snapshots, state snapshots, employer/client data, customer data, regulated
data, internal URLs, or approval records.

Generated outputs inherit source sensitivity. Private-derived outputs remain
private by default and require separate human review before any sharing.

