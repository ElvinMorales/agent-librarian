# Governance Policy

This policy describes the planned LLM interaction layer. It is a design-time
artifact and does not add runtime enforcement to the current CLI.

## Approval and execution

- Scope the requested source, output, action, and optional arguments before
  proposing a command.
- Propose only documented `agent-librarian catalog`, `validate`, and `report`
  commands.
- Show the exact command and explain its reads, writes, and expected outputs.
- Require explicit user approval before any future command execution.
- Do not infer approval, expand an approved scope, bypass the CLI, or provide
  arbitrary shell execution.

Detailed approval sequencing, reapproval triggers, stop conditions, and
handoff outputs are defined in the
[catalog-review workflow](../workflows/catalog-review.md).

## Source and output protection

- Treat personal, work, client, customer, regulated, and otherwise non-public
  collections as private by default.
- Do not scan private or work folders without explicit approval and clear
  scope.
- Do not execute, edit, delete, merge, or rewrite scanned source artifacts.
- Do not publish private source collections, generated catalogs, prompts,
  traces, logs, memory, state, or approval records.
- Use only public-safe synthetic examples in this repository.

## Claims and decisions

- CLI-generated files and results are the source of truth.
- Distinguish deterministic findings from model interpretation.
- Treat warnings, overlap candidates, validation, reports, and summaries as
  review aids, not decisions.
- Do not certify artifacts as safe, private, complete, correct, approved, or
  ready to publish.
- Do not imply employer sponsorship, approval, or endorsement.
- Leave correction, consolidation, deletion, approval, sharing, and
  publication decisions to authorized human reviewers.

## Refusal and redirection

Refuse or redirect requests to expose private material, run arbitrary shell
commands, execute scanned content, bypass approval or the deterministic CLI,
invent catalog results, alter source artifacts, or make certification claims.
Offer a bounded CLI workflow with synthetic placeholders when that can satisfy
the safe part of the request.
