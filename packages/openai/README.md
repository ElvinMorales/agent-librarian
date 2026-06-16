# OpenAI Package

This package adapts the canonical `agent-librarian` contract for OpenAI
workspaces without changing the deterministic CLI backend.

The source of truth remains under `agent/`. OpenAI package files are
adapters for Codex, GPT, and ChatGPT Projects; they do not define separate
agent identities.

## Package Contents

- `codex/AGENTS.md`: Codex-native project instructions for local,
  approval-gated demos.
- `codex/.agents/skills/artifact-librarian/SKILL.md`: Codex skill for the
  synthetic Agent Librarian workflow.
- `codex/codex-demo-prompt.md`: public-safe prompt for invoking the Codex
  demo.
- `codex/codex-validation-checklist.md`: validation checklist for the Codex
  package.
- `gpt/`: advisory GPT instructions, knowledge manifest, conversation
  starters, and future Actions notes.
- `chatgpt-project/`: advisory ChatGPT Project instructions and source-file
  upload guidance.

## Local vs Advisory

The Codex package is command-capable only when Codex is running in a local
workspace with appropriate sandbox and approval controls. It must prefer
runtime-wrapper `propose` before `run`, require exact approval before wrapper
`run`, and summarize only deterministic evidence.

The GPT and ChatGPT Project packages are advisory. Regular GPT chats and
ChatGPT Projects do not run the local CLI by default. They can explain,
review, and guide next steps using uploaded or pasted source-of-truth files,
but they must not claim local command execution unless a future reviewed
Action/API wrapper exists.

## Boundaries

Use only the synthetic `examples/sample-collection` for public demos. Do not
scan or upload private scans, private generated outputs, work folders,
secrets, credentials, private journals, private prompts, private traces,
memory snapshots, state snapshots, employer/client data, or internal URLs.

The OpenAI package does not add OpenAI API integration, network behavior, MCP
server code, arbitrary shell execution, CLI behavior changes, schema changes,
generated-output changes, release behavior, or package version changes.

