# One Agent Librarian contract, multiple LLM workspaces.

This guide shows the v0.5 portable package demo paths across LLM workspaces.
Lead with the working workflow: an LLM workspace acts as the interface layer,
the deterministic `agent-librarian` CLI remains the source of truth, and a
human reviews the generated evidence.

The platform changes. The agent contract does not.

## Shared Overview

All package paths preserve the same contract:

```text
LLM workspace explains safe scope
-> LLM workspace proposes or requests deterministic evidence
-> exact approval gates local execution when local tools exist
-> deterministic CLI outputs remain source of truth
-> LLM workspace summarizes bounded evidence
-> human reviews warnings, overlap candidates, and publication risk
```

The shared public demo scope is:

```text
examples/sample-collection
examples/generated-catalog
```

Do not use private, work-internal, customer, regulated, trace, log, memory,
state, credential, secret-bearing, employer-specific, or client-specific
material for public demos.

## Claude Code Path

Use the Claude Code package for a command-capable local demo:

- project instructions: `packages/claude/CLAUDE.md`
- skill: `packages/claude/claude-code/.claude/skills/artifact-librarian-demo/SKILL.md`
- prompt: `packages/claude/claude-code/demo-prompt.md`
- guide: `docs/demos/claude-code-end-to-end.md`

Flow:

```text
Claude Code reads package instructions
-> Claude explains safe scope
-> Claude proposes runtime-wrapper commands
-> user approves exact command
-> wrapper runs deterministic CLI backend
-> Claude summarizes CLI evidence
-> human reviews generated outputs
```

## Codex Path

Use the Codex package for the same command-capable local demo in a Codex
workspace:

- project instructions: `packages/openai/codex/AGENTS.md`
- skill: `packages/openai/codex/.agents/skills/artifact-librarian/SKILL.md`
- prompt: `packages/openai/codex/codex-demo-prompt.md`
- guide: `docs/demos/codex-end-to-end.md`

Flow:

```text
Open Codex in the repo
-> Codex reads AGENTS.md
-> user invokes or references the artifact-librarian skill
-> Codex proposes runtime-wrapper command
-> user approves exact command
-> wrapper runs deterministic CLI
-> Codex summarizes generated outputs
```

## GPT and ChatGPT Advisory Path

Use the GPT or ChatGPT Project package for advisory review:

- GPT instructions: `packages/openai/gpt/instructions.md`
- GPT knowledge manifest: `packages/openai/gpt/knowledge-manifest.md`
- GPT conversation starters: `packages/openai/gpt/conversation-starters.md`
- ChatGPT Project instructions:
  `packages/openai/chatgpt-project/project-instructions.md`
- ChatGPT Project upload list:
  `packages/openai/chatgpt-project/source-files-to-upload.md`
- guide: `docs/demos/gpt-chat-end-to-end.md`

Flow:

```text
User uploads or pastes public-safe generated outputs
-> GPT or ChatGPT Project explains the workflow
-> chat reviews deterministic evidence
-> chat asks the user to run local commands when evidence is missing
-> human reviews generated outputs and publication risk
```

Regular GPT chats and ChatGPT Projects do not run the local CLI by default.
They must not claim local command execution unless a future reviewed
Action/API wrapper exists.

## Exact Demo Commands

Command-capable packages should propose before running:

```bash
python -m agent_librarian.runtime_wrapper propose catalog examples/sample-collection --out examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose validate examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose report examples/generated-catalog
```

Wrong approval must fail without executing the deterministic backend:

```bash
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "wrong command"
```

Correct approval for the read-only report demo:

```bash
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "agent-librarian report examples/generated-catalog"
```

Advisory GPT/ChatGPT packages should ask the user to run local evidence
commands when needed:

```bash
agent-librarian validate examples/generated-catalog
agent-librarian report examples/generated-catalog
```

## What Is Shared Across Packages

- canonical identity and behavior under `agent/`
- bounded `catalog`, `validate`, and `report` command contract
- exact approval rule for local execution
- deterministic CLI outputs as source of truth
- generated outputs inherit source sensitivity
- summaries remain secondary review aids
- publication requires separate human review
- no safety, privacy, correctness, completeness, approval, compliance, or
  publication-readiness certification

## What Differs by Platform

- Claude Code uses `CLAUDE.md` and a Claude Code skill.
- Codex uses `AGENTS.md` and a Codex skill.
- GPT uses builder-style advisory instructions and uploaded knowledge files.
- ChatGPT Projects use project instructions and source-file upload guidance.
- Command-capable local workspaces may run the runtime wrapper after exact
  approval.
- Advisory chat workspaces review uploaded or pasted evidence and suggest
  local commands without claiming execution.

## Public-Safety Warnings

Use only synthetic examples for public demos. Do not scan or upload private
scans, private generated outputs, work folders, secrets, credentials, private
journals, private prompts, private traces, memory snapshots, state snapshots,
approval logs, runtime records, employer/client data, customer data,
regulated data, or internal URLs.

Generated outputs inherit source sensitivity. Private-derived outputs remain
private by default and require separate authorized human review before any
sharing or publication.

## What This Is Not

This is not an OpenAI API integration, Claude API integration, MCP server,
network service, hosted agent runtime, arbitrary shell, publication system, or
certification process.

This does not prove autonomous safety, privacy, correctness, completeness,
compliance, approval, publication readiness, or production readiness.

## Portable-Agent Thesis

The demo supports the portable-agent thesis in plain terms: one bounded Agent
Librarian contract can be adapted into multiple LLM workspaces while keeping
the same deterministic evidence, approval gate, and human-review boundary.

The value is not a new taxonomy. The value is that the same working contract
can show up as Claude Code instructions, Codex project instructions, or
advisory GPT/ChatGPT guidance without forking the agent.
