# Claude Code End-to-End Demo

This guide runs the Claude package as a functional agent-shaped demo:

```text
Claude Code reads package instructions
-> Claude explains safe scope
-> Claude proposes runtime-wrapper commands
-> user approves exact command
-> wrapper runs deterministic CLI backend
-> Claude summarizes CLI evidence
-> human reviews generated outputs
```

The demo does not add Claude API integration, network behavior, MCP server
code, arbitrary shell execution, source modification, schema changes, or
generated-output changes.

## Setup

From a tagged release:

```bash
git checkout TAG_NAME
python -m pip install -e ".[dev]"
```

From a current checkout:

```bash
python -m pip install -e ".[dev]"
```

Confirm the CLI is available:

```bash
agent-librarian --version
agent-librarian --help
```

## Claude Code Package

Use `packages/claude/CLAUDE.md` as the project instruction file for Claude
Code. If your Claude Code setup expects instructions at the workspace root,
copy that file to root `CLAUDE.md` for the demo.

Use the skill at:

```text
packages/claude/claude-code/.claude/skills/artifact-librarian-demo/SKILL.md
```

Invoke it with:

```text
packages/claude/claude-code/demo-prompt.md
```

## Expected Commands

Claude should propose these commands before any run:

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

Expected result: the wrapper exits with a nonzero status and does not run the
backend report command.

## Correct Approval Demo

After Claude shows the exact command and scope, approve and run:

```bash
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "agent-librarian report examples/generated-catalog"
```

Claude should summarize the actual report output only. It should not invent
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

These generated files and CLI output are the source of truth. Claude's summary
is a secondary review aid.

## Talk Track

Claude is acting as the interface layer. It explains that the demo uses only
synthetic files, proposes bounded wrapper commands, asks for exact approval,
and summarizes deterministic evidence.

The runtime wrapper enforces the approval gate. The deterministic CLI reads
the selected catalog files and reports diagnostics, warnings, and overlap
candidates. A human reviewer decides what the evidence means.

## Troubleshooting

- If `agent-librarian` is not found, run `python -m pip install -e ".[dev]"`.
- If the wrong approval command succeeds, stop the demo and inspect the
  wrapper; the expected behavior is a nonzero exit without backend execution.
- If generated files changed unexpectedly, inspect
  `git diff -- examples/generated-catalog`.
- If Claude proposes arbitrary shell, source modification, or a broader scan,
  stop and return to `packages/claude/CLAUDE.md`.

## Safety Warnings

Do not scan private, work-internal, customer, regulated, trace, log, memory,
state, credential, or secret-bearing material for public demos. Do not include
employer-specific examples, internal URLs, private prompts, private traces,
memory snapshots, state snapshots, or private generated catalogs.

Validation and reports are review aids. They do not certify safety,
correctness, completeness, approval, compliance, or publication readiness.
