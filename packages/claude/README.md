# Claude Package

This package adapts the canonical `agent-librarian` agent contract for Claude
workspaces without changing the deterministic CLI backend.

The working demo story is:

```text
Claude Code reads package instructions
-> Claude explains safe scope
-> Claude proposes runtime-wrapper commands
-> user approves exact command
-> wrapper runs deterministic CLI backend
-> Claude summarizes CLI evidence
-> human reviews generated outputs
```

Claude is the interface layer. The deterministic CLI, runtime-wrapper output,
and generated catalog files remain the source of truth.

## Package Contents

- `CLAUDE.md`: reusable Claude Code project instructions.
- `claude-code/.claude/skills/artifact-librarian-demo/SKILL.md`: a demo skill
  for the synthetic end-to-end workflow.
- `claude-code/demo-prompt.md`: a public-safe prompt for invoking the demo.
- `claude-code/install.md`: copy/use instructions for Claude Code.
- `claude-enterprise/`: public-safe adaptation notes for managed
  instructions, admin review, and private deployments.
- `cowork/`: plain-language cowork demo script and user-facing guardrails.

## Boundaries

Use only the synthetic `examples/sample-collection` for public demos. Do not
scan private, work-internal, customer, regulated, trace, log, memory, state,
credential, or secret-bearing material for public examples.

The Claude package does not add Claude API integration, MCP server code,
network behavior, arbitrary shell execution, CLI behavior changes, schema
changes, generated-output changes, release behavior, or package version
changes.

For the runnable guide, see
[`docs/demos/claude-code-end-to-end.md`](../../docs/demos/claude-code-end-to-end.md).

