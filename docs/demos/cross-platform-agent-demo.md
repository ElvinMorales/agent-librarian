# Cross-Platform Agent Demo

This guide tracks the v0.5 portable package demo paths across LLM workspaces.
Only the Claude package is implemented in this goal. Other platform sections
remain placeholders until their package adapters exist.

## Claude Code

Use the Claude Code package for the current end-to-end demo:

- project instructions: `packages/claude/CLAUDE.md`
- skill: `packages/claude/claude-code/.claude/skills/artifact-librarian-demo/SKILL.md`
- prompt: `packages/claude/claude-code/demo-prompt.md`
- guide: `docs/demos/claude-code-end-to-end.md`

The demo flow is:

```text
Claude Code reads package instructions
-> Claude explains safe scope
-> Claude proposes runtime-wrapper commands
-> user approves exact command
-> wrapper runs deterministic CLI backend
-> Claude summarizes CLI evidence
-> human reviews generated outputs
```

Use only `examples/sample-collection` and `examples/generated-catalog` for
public demos.

## Claude Enterprise

Claude Enterprise adaptation is advisory in this repository. See
`docs/demos/claude-enterprise-adaptation.md` and the notes under
`packages/claude/claude-enterprise/`.

Managed instructions, approved workflow bundles, approval logs, and private
retention policies should be reviewed in the private environment before any
work-internal use.

## Claude Cowork

Cowork-facing material is available under `packages/claude/cowork/`. It
explains the demo in plain language, what can be shown, what must not be
scanned, exact approval, and how to answer whether the workflow is autonomous.

## Codex

Planned placeholder. Add this section when a Codex package exists.

## GPT

Planned placeholder. Add this section when a GPT package exists.

## ChatGPT Project

Planned placeholder. Add this section when a ChatGPT Project package exists.

