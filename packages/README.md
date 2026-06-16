# Agent Package Adapters

This directory contains portable package scaffolding for adapting the
canonical `agent-librarian` contract to different LLM workspaces.

The source of truth remains under `agent/`. Files under `packages/` must be
adapters, not separate agent definitions.

```text
agent/
  -> shared package manifest and conformance expectations
  -> packages/
```

## Current Status

v0.5 adds the shared package foundation:

- `shared/package-manifest.schema.json`
- `shared/package-manifest.example.yaml`
- `shared/conformance/`

It also adds the first platform adapter:

- `claude/README.md`
- `claude/CLAUDE.md`
- `claude/claude-code/.claude/skills/artifact-librarian-demo/SKILL.md`
- `claude/claude-code/demo-prompt.md`
- `claude/claude-code/install.md`
- `claude/claude-enterprise/`
- `claude/cowork/`

The Claude Code package demonstrates a functional local workflow using the
approval-gated runtime wrapper and deterministic CLI evidence. Claude
Enterprise and Cowork materials are public-safe adaptation notes and do not
claim local execution from this repository.

Codex, GPT, and ChatGPT Project package files are still planned.

## Package Rules

Package adapters must preserve the canonical contract:

- CLI-generated files and command outputs remain the source of truth.
- Local execution requires exact command approval.
- Advisory-only packages must not claim local command execution.
- Generated outputs inherit source sensitivity.
- Review summaries are secondary review aids.
- Publication requires separate human review.
- No adapter may add arbitrary shell execution, provider integration, MCP
  servers, network behavior, source modification, or certification claims.

See [Portable Agent Packages](../docs/portable-agent-packages.md) for the
architecture.

See [Claude Code End-to-End Demo](../docs/demos/claude-code-end-to-end.md) for
the runnable Claude package demo.

