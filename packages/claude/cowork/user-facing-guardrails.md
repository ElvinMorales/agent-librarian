# User-Facing Guardrails

Use these guardrails in cowork demos and shared notes.

## What You Can Safely Show

- The synthetic source fixture: `examples/sample-collection`
- The generated synthetic catalog: `examples/generated-catalog`
- The Claude package instructions under `packages/claude/`
- Runtime-wrapper proposal JSON for the synthetic fixture
- The wrong-command approval failure
- The read-only report command after exact approval

## What Not to Scan

Do not scan or show:

- private or work-internal folders
- customer, client, regulated, or personal data
- credentials, secrets, tokens, or internal URLs
- private prompts, private traces, logs, memory snapshots, or state snapshots
- approval logs or generated catalogs from private scans

## How to Explain Exact Approval

Exact approval means the user approves the specific visible command and scope.
If the command, path, argument, sensitivity, or retry changes, approval must be
requested again.

This prevents a broad "go ahead" from becoming permission to run a different
command or scan a wider folder.

## How to Answer "Is This an Autonomous Agent?"

Say: it is a bounded agent workflow, not an autonomous operator. Claude helps
with scoping, explanation, command proposal, approval handoff, and evidence
summary. The deterministic CLI and generated outputs remain the source of
truth, and a human remains responsible for review and sharing decisions.

Do not say it certifies safety, correctness, completeness, approval,
compliance, or publication readiness.

