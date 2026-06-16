# Portable Agent Packages

## Purpose

v0.5 starts the portable package foundation for `agent-librarian`.

```text
One agent contract, multiple LLM-native package adapters.
```

The canonical agent artifacts stay under `agent/`. Package adapters under
`packages/` will translate that same contract into the file shapes expected by
specific LLM workspaces. This avoids maintaining separate agent definitions
for Claude, Codex, GPT, ChatGPT Projects, or future hosts.

This workstream is architecture and shared package scaffolding only. It does
not add provider integration, an MCP server, network behavior, new CLI
behavior, or platform package implementations.

## Why v0.5 Exists

v0.4 made the planned interaction layer inspectable: identity, operating
principles, tool boundaries, approval workflow, public-safety policy, runtime
state design, safe-scan evals, and review-summary schema all live under
`agent/`.

v0.5 adds the packaging layer needed to reuse that contract in multiple LLM
workspaces without forking the agent. The same source-of-truth artifacts can
be adapted into workspace-native instructions, skill files, project
instructions, or advisory prompts while keeping deterministic CLI evidence
and approval rules shared.

## Canonical Artifacts vs Platform Packages

Canonical artifacts define the agent contract:

- framework-neutral identity and operating principles
- bounded CLI tool contract
- catalog-review workflow
- public-safety and refusal policy
- safe-scan eval cases
- runtime state and approval-log expectations
- review-summary output schema

Platform packages are adapters. They may reorganize, summarize, or format the
canonical contract for a host workspace, but they must not become separate
agents with independent policies or command surfaces.

The repository pattern is:

```text
canonical agent artifacts under agent/
  -> shared package manifest and conformance expectations
  -> platform-specific packages under packages/
```

## Source of Truth

`agent/` remains the source of truth because it contains the shared behavior
that every package must preserve:

- identify as Agent Librarian, a local-first assistant for cataloging and
  reviewing agentic AI artifacts
- propose only documented `agent-librarian` commands
- require exact approval before local execution
- treat generated outputs as inheriting source sensitivity
- keep CLI-generated files and command output as authoritative evidence
- keep model-authored summaries secondary to deterministic outputs
- refuse arbitrary shell, source modification, unsafe publication, and
  certification claims

Adapters may point to platform-specific files, but if an adapter conflicts
with `agent/`, the canonical `agent/` contract wins.

The framework-neutral identity source is
[`agent/identity.md`](../agent/identity.md). Claude, Codex, GPT, and ChatGPT
packages adapt that same identity; they do not create separate agents.

## Package Targets

The shared manifest schema recognizes these package targets:

- `claude-code`
- `claude-enterprise`
- `claude-cowork`
- `codex`
- `gpt`
- `chatgpt-project`
- `shared`

The targets differ by how much local action they can safely expose.

| Target | Expected package shape | Local command execution today | Current package status |
| --- | --- | --- | --- |
| Claude Code | Workspace instructions and a Claude Code skill | Command-capable when the host workspace grants local tools and the adapter enforces exact approval | Planned only |
| Claude Enterprise | Enterprise-managed instructions, policy notes, or knowledge content | Advisory-only in this repo; enterprise tool access must be separately reviewed | Planned only |
| Claude Cowork | Cowork-oriented shared instructions or collaboration guidance | Advisory-only in this repo unless a separately governed host provides tools | Planned only |
| Codex | `AGENTS.md` and Codex skill packaging | Command-capable when running in a local workspace with sandbox and approval controls | Planned only |
| GPT | Builder/custom GPT instructions and reference files | Advisory-only; no local filesystem or CLI execution is claimed by this repo | Planned only |
| ChatGPT Project | Project instructions and reference docs | Advisory-only; no local filesystem or CLI execution is claimed by this repo | Planned only |
| Shared | Manifest schema, examples, and conformance expectations | Does not execute commands | Added in v0.5 |

No v0.5 platform adapter file is treated as a live provider integration. The
only current executable surfaces remain the deterministic CLI and the optional
local runtime wrapper prototype documented in
[`docs/runtime-wrapper-prototype.md`](runtime-wrapper-prototype.md).

## Command-Capable vs Advisory Packages

Command-capable packages may describe local execution only when the host
workspace actually supports local command tools and the adapter preserves the
canonical approval contract. Today, that category is limited to future Claude
Code and Codex adapters.

Advisory packages must not claim they can run `agent-librarian`, inspect local
files, validate a local catalog, or generate local outputs. Today, future GPT,
ChatGPT Project, Claude Enterprise, and Claude Cowork packages are
advisory-only from this repository's perspective unless a separate governed
runtime is introduced.

All packages, including command-capable ones, must preserve this rule:

```text
No execution without exact command approval.
```

## Future MCP, API, and Tool Exposure

MCP servers, hosted APIs, provider tools, and workspace-specific execution
bridges are future work. They are not part of v0.5.

Future tool exposure must be separately designed and reviewed because it would
change the enforcement surface. It must still preserve the existing command
contract:

- only `catalog`, `validate`, and `report`
- no arbitrary shell
- no source execution or modification
- exact approval for the visible command and scope
- generated outputs inherit source sensitivity
- validation and reports remain review aids, not certifications

## Shared Evidence and Approval Contract

Every package adapter must keep these shared evidence rules:

- The deterministic CLI remains the source of truth for generated catalogs,
  diagnostics, overlap reports, validation, and report output.
- The optional runtime wrapper remains a bounded local harness, not an LLM
  provider integration.
- Approval applies only to the exact command, paths, optional arguments, read
  scope, write scope, and sensitivity warning shown to the user.
- Changed commands, paths, optional arguments, scope, sensitivity, or retry
  behavior require fresh approval.
- Model-authored summaries must follow the review-summary contract when saved
  and must remain secondary review aids.
- Publication requires separate human review.

## Shared Package Artifacts

The shared package foundation lives under `packages/shared/`:

- `package-manifest.schema.json` defines the lightweight manifest contract
  for package adapters.
- `package-manifest.example.yaml` shows how canonical sources map to planned
  platform package files.
- `conformance/` records scenario expectations that every adapter must
  preserve.

These files establish conformance expectations only. They do not create
Claude, Codex, GPT, or ChatGPT package implementations.

## Public-Safe Examples

Package examples must remain synthetic and public-safe. Use placeholders such
as `PRIVATE_SOURCE`, `PRIVATE_OUTPUT`, and `PRIVATE_CATALOG` for private-local
flows. Do not include real private paths, employer-specific workflows,
customer data, secrets, credentials, traces, logs, memory snapshots, approval
records, or generated private catalogs in package artifacts.
