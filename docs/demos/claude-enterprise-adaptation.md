# Claude Enterprise Adaptation

This guide describes public-safe adaptation paths for Claude Enterprise. It
does not include employer-specific examples, private data, internal URLs,
private prompts, traces, logs, memory snapshots, or state snapshots.

## Public Demo Package vs Private Adaptation

The public Claude package demonstrates the workflow with:

```text
examples/sample-collection
examples/generated-catalog
```

A private/work adaptation may use authorized internal collections, but private
source files and derived outputs stay private. Public docs should use
placeholders such as:

```text
PRIVATE_SOURCE
PRIVATE_OUTPUT
PRIVATE_CATALOG
```

## Managed Instructions vs Project Instructions

Project instructions are useful for a single Claude Code checkout, such as
`packages/claude/CLAUDE.md`.

Managed instructions are better for enterprise adaptation because they can
standardize:

- source-of-truth wording
- exact approval requirements
- private/work-internal handling
- allowed workflow bundles
- evidence and logging expectations
- review routing before sharing

If project instructions and managed instructions conflict, the stricter
safety and approval rule should win.

## Skills as Approved Workflow Bundles

Skills can package a bounded workflow:

1. explain scope
2. propose allowed commands
3. require exact approval
4. run only through an approved local wrapper when available
5. summarize deterministic evidence
6. hand results to human review

Skills should not add arbitrary shell execution, source modification, network
behavior, MCP/API exposure, or publication authority.

## Approval and Logging Expectations

Private deployments should define:

- who can request scans
- who can approve exact commands
- approved source and output locations
- where approval logs and execution records are stored
- how generated outputs are reviewed
- how private outputs and records are retained or deleted
- when separate sharing or publication review is required

Approval logs, execution records, generated catalogs, reports, and summaries
inherit source sensitivity.

## What to Keep Private

Keep these out of public package files and public demos:

- private or work-internal source collections
- internal URLs
- credentials, secrets, and tokens
- private prompts
- private traces and logs
- memory snapshots and state snapshots
- private approval logs and execution records
- generated outputs from private scans

## Why MCP/API Exposure Is Future Review Work

MCP servers, Claude API integrations, hosted services, provider tools, and
network bridges change the enforcement surface. They require separate design
and review before use.

This package deliberately does not add MCP server code, Claude API calls,
network behavior, CLI/runtime behavior changes, schema changes, or generated
output changes.

## Public-Safe Safety Checklist

- Use synthetic examples in public demos.
- State that Claude is the interface layer.
- State that deterministic CLI evidence is the source of truth.
- Prefer wrapper `propose` before `run`.
- Require exact approval before execution.
- Refuse arbitrary shell and source modification.
- Do not certify safety, correctness, completeness, approval, compliance, or
  publication readiness.
- Require human review before sharing any generated outputs.

