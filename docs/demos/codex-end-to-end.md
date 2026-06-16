# Codex End-to-End Demo

This guide runs the Codex package as a functional agent-shaped demo:

```text
Open Codex in the repo
-> Codex reads AGENTS.md
-> user invokes or references the artifact-librarian skill
-> Codex proposes runtime-wrapper command
-> user approves exact command
-> wrapper runs deterministic CLI
-> Codex summarizes generated outputs
```

The demo does not add OpenAI API integration, network behavior, MCP server
code, arbitrary shell execution, source modification, schema changes, or
generated-output changes.

## Setup

From a current checkout:

```bash
python -m pip install -e ".[dev]"
```

Confirm the CLI is available:

```bash
agent-librarian --version
agent-librarian --help
```

Open Codex in the repository and use:

```text
packages/openai/codex/AGENTS.md
packages/openai/codex/.agents/skills/artifact-librarian/SKILL.md
packages/openai/codex/codex-demo-prompt.md
```

If your Codex setup expects project instructions at the workspace root, copy
or reference `packages/openai/codex/AGENTS.md` for the demo.

## Expected Proposal Commands

Codex should propose these commands before any run:

```bash
python -m agent_librarian.runtime_wrapper propose catalog examples/sample-collection --out examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose validate examples/generated-catalog
python -m agent_librarian.runtime_wrapper propose report examples/generated-catalog
```

The proposal output should show the exact backend command, expected reads,
expected writes, generated files, sensitivity class, exact approval
instruction, source-protection note, and non-certification note.

## Wrong Approval Failure

Demonstrate that a mismatched approval blocks execution:

```bash
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "wrong command"
```

Expected result: the wrapper exits with a nonzero status and does not execute
the deterministic backend report command. Do not require a specific exit
code.

## Correct Approval Demo

After Codex shows the exact command and scope, approve and run:

```bash
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "agent-librarian report examples/generated-catalog"
```

Codex should summarize the actual report output only. It should not invent
findings or claim the catalog is safe, correct, complete, approved, or ready
to publish.

## Files to Show

After execution, point human reviewers to:

```text
examples/generated-catalog/index.json
examples/generated-catalog/catalog.md
examples/generated-catalog/diagnostics.json
examples/generated-catalog/overlap-report.json
```

These generated files and CLI output are the source of truth. Codex's summary
is a secondary review aid.

## Safety Warnings

Do not scan private, work-internal, customer, regulated, trace, log, memory,
state, credential, or secret-bearing material for public demos. Do not include
employer-specific examples, internal URLs, private prompts, private traces,
memory snapshots, state snapshots, or private generated catalogs.

Validation and reports are review aids. They do not certify safety,
correctness, completeness, approval, compliance, or publication readiness.

