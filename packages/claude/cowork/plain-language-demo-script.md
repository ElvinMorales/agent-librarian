# Plain-Language Demo Script

Use this script when showing the Claude Code demo to a cowork.

## Opening

This is a local demo of an artifact librarian. Claude is not cataloging files
by itself. Claude explains the safe scope, proposes exact wrapper commands,
waits for approval, and summarizes what the deterministic CLI reports.

The source of truth is the CLI output and the generated files, not Claude's
summary.

## Safe Demo Scope

We are only using the synthetic sample collection in:

```text
examples/sample-collection
```

The generated catalog is in:

```text
examples/generated-catalog
```

We are not scanning private folders, work-internal files, customer material,
credentials, secrets, private prompts, traces, logs, memory snapshots, or
state snapshots.

## Exact Approval

Claude first proposes a command and explains what it reads and writes. The
wrapper then requires an approval string that exactly matches the command it
plans to run.

If the approval string is wrong, the wrapper exits without running the
backend. That is intentional. It shows that broad intent or vague approval is
not enough.

## Is This an Autonomous Agent?

It is agent-shaped, but bounded. Claude scopes the request, explains safety,
proposes commands, asks for exact approval, and summarizes deterministic
evidence. It does not have authority to run arbitrary shell, scan outside the
approved scope, publish outputs, approve artifacts, or certify that results
are safe or complete.

## Closing

The useful part is the separation of duties: Claude handles the human-facing
workflow, the wrapper enforces exact approval, the CLI creates deterministic
evidence, and a human reviews the outputs.

