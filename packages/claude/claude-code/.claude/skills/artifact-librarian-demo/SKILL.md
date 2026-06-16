---
name: artifact-librarian-demo
description: Run a safe public demo of the agent-librarian workflow using the synthetic sample collection, approval-gated runtime wrapper, deterministic CLI outputs, and human-review summary.
disable-model-invocation: true
---

# Artifact Librarian Demo

Use this skill to run a public-safe Claude Code demo of `agent-librarian`.
Lead with the functional agent story, not taxonomy.

## Workflow

```text
Claude Code reads package instructions
-> Claude explains safe scope
-> Claude proposes runtime-wrapper commands
-> user approves exact command
-> wrapper runs deterministic CLI backend
-> Claude summarizes CLI evidence
-> human reviews generated outputs
```

## Steps

1. Explain the agent in plain language.
   - Claude is the interface layer.
   - The deterministic CLI and generated outputs are the source of truth.
   - The demo uses only the synthetic `examples/sample-collection`.

2. Inspect only allowed public demo files.
   - Allowed source: `examples/sample-collection`.
   - Allowed generated catalog: `examples/generated-catalog`.
   - Allowed package instructions: `packages/claude/`.
   - Do not scan private/work files, work-internal folders, credentials,
     secrets, private prompts, private traces, logs, memory snapshots, state
     snapshots, or private generated catalogs.

3. Propose commands before running anything.
   - Prefer runtime-wrapper `propose` commands.
   - Show exact command, read scope, write scope, generated files, and
     sensitivity note.

4. Require exact approval.
   - Do not run on vague approval.
   - Do not run if the approval string is different from the command shown.
   - Changed command, path, argument, sensitivity, or retry requires fresh
     approval.

5. Run only approved wrapper commands.
   - Do not run arbitrary shell.
   - Do not chain commands.
   - Do not execute, edit, delete, merge, publish, or rewrite source files.
   - Do not create git commits, pushes, tags, releases, or pull requests.

6. Summarize deterministic outputs.
   - Use runtime-wrapper output, CLI output, and generated files as evidence.
   - Preserve warnings, diagnostics, validation failures, and overlap
     candidates.
   - Do not invent counts, files, findings, or status.

7. Explain what the demo proves.
   - Claude can scope a synthetic public demo.
   - Claude can propose bounded wrapper commands.
   - Exact approval gates local execution.
   - The deterministic backend produces evidence for human review.

8. Explain what the demo does not prove.
   - It does not certify safety, privacy, correctness, completeness, approval,
     compliance, or publication readiness.
   - It does not scan private or work-internal material.
   - It does not add Claude API integration, network behavior, MCP server
     code, arbitrary shell execution, or autonomous publication.

## Allowed Demo Commands

```bash
python -m agent_librarian.runtime_wrapper propose catalog examples/sample-collection --out examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose validate examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose report examples/generated-catalog
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "agent-librarian report examples/generated-catalog"
```

Wrong approval demonstration:

```bash
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "wrong command"
```

The wrong approval should fail with a nonzero exit status and must not run the
backend.
