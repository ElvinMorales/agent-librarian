# Claude Enterprise Managed Instructions

These public-safe notes show how an organization could adapt the
`agent-librarian` contract into managed Claude Enterprise instructions. They
are advisory only in this repository.

## Managed Instruction Shape

Use managed instructions to preserve shared behavior across approved
workspaces:

- Claude is the interface layer, not the source of truth.
- Deterministic CLI outputs and generated files are the source of truth.
- Public demos use only synthetic examples.
- Private or work-internal scans require narrow scope, authorization, and
  private handling.
- Exact approval is required before any approved local execution surface runs.
- Validation and reports are review aids, not safety, correctness,
  completeness, approval, or publication certification.

## Project Instructions vs Managed Instructions

Project instructions such as `packages/claude/CLAUDE.md` are suitable for a
single public demo checkout. Managed instructions are better for repeatable
private/work adaptation because administrators can standardize safety
language, approved tool surfaces, logging expectations, and review routing.

Project instructions should not override managed policy. If they conflict,
the stricter private-handling, approval, and source-of-truth rule should win.

## Skills as Approved Workflow Bundles

Claude skills can package a known workflow:

- explain scope
- propose approved commands
- require exact approval
- run only through an approved local wrapper when available
- summarize deterministic evidence
- hand results to a human reviewer

Skills should not add arbitrary shell access, source modification, network
behavior, MCP exposure, or publication authority.

## Approval and Logging Expectations

Private deployments should define:

- exact command approval wording
- approved source and output paths
- sensitivity classes
- where approval records are stored
- who can approve private or work-internal scans
- retention and deletion expectations for generated outputs and records
- review steps before any sharing

Approval logs and generated outputs inherit source sensitivity and must not be
used as public examples.

## Future Tool Exposure

MCP, API, provider tools, hosted services, and enterprise automation are
future review work. They change the enforcement surface and should be
designed separately before use.

This package does not add MCP server code, Claude API calls, network
behavior, or new CLI/runtime behavior.

