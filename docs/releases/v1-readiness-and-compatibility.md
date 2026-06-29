# v1.0 Readiness and Compatibility Contract

Status: Reviewed for v1.0.0 release preparation. The actual tag and GitHub
release remain maintainer actions.

Applies to: core `agent-librarian` repository.

Does not apply to: live provider-specific companion adapters except at their
source snapshot output boundary.

This document defines the readiness and compatibility boundary for
[`agent-librarian`](../../README.md) v1.0. It is a governance artifact, not a
release: it does not create a tag, publish an artifact, certify readiness, or
approve the release. Issue
[#100](https://github.com/ElvinMorales/agent-librarian/issues/100) prepares the
release files; a maintainer reviews and performs tag and release actions
separately.

## What v1.0 Means

v1.0 is a stable public reference implementation for deterministic local
artifact cataloging, package adapter validation, presentation of generated
catalog outputs, and governed external-source snapshot handling.

Core `agent-librarian` remains local-first and provider-neutral. External
systems become local, reviewable source snapshots before cataloging.

Stable means that consumers can build against the documented purposes and
general structures in this contract. It does not mean that every schema field,
diagnostic, presentation section, adapter mapping, or check is frozen forever.

## Readiness Criteria

All criteria in this section must be true before v1.0.0 release preparation is
completed.

### Deterministic CLI

- `catalog` produces deterministic catalog facts for the same local inputs,
  options, and supported runtime conditions.
- `validate` checks generated JSON outputs against the bundled schemas without
  modifying them.
- `report` summarizes generated catalog facts for human review without
  rescanning or modifying source inputs.
- The default `present` path remains offline and deterministic and renders only
  generated catalog facts.
- Optional narration, if present, remains an explicit opt-in, is labeled as
  model-authored, and records provenance.
- Commands fail clearly and avoid partial unsafe writes. When a documented mode
  intentionally writes review artifacts before returning a nonzero status,
  such as strict cataloging with parse failures, that behavior remains explicit.
- No default command requires network access, provider credentials, or a live
  external source.

### Generated Outputs and Schemas

- Generated catalog output paths and meanings are documented.
- JSON outputs validate against their documented bundled schemas.
- Schema changes are intentional, tested, and documented in the changelog.
- Generated outputs inherit the sensitivity of their source or input.
- Generated outputs, validation results, warnings, overlap candidates, reports,
  and presentations are review aids. They are not certification or approval.

### Portable Package Adapters

- Claude Code, Codex, GPT, and ChatGPT Project package surfaces remain
  documented, including which surfaces are command-capable and which are
  advisory-only.
- The canonical framework-neutral agent contract remains under `agent/`, the
  shared package contract remains under `packages/shared/`, and provider
  mappings remain adapters under `packages/` rather than independent agents.
- Package conformance checks pass.
- Public package examples are synthetic and framework-neutral where practical.
- Package adapters contain no private logs, traces, secrets, credentials, or
  unsanitized memory or runtime state.

### Presentation Layer

- Offline `overview.html` generation remains deterministic for unchanged
  generated JSON inputs.
- Presentation reads generated catalog facts rather than source files or
  private source systems.
- Narrated output, if used, remains labeled, secondary to deterministic facts,
  and backed by `narrative-provenance.json`.
- Presentation does not imply safety, correctness, completeness, compliance,
  publication approval, or production readiness.

### Source Snapshot Contract

- An external source is represented locally as `files/` plus
  `source-manifest.json` before core cataloging begins.
- The manifest records approved scope, exclusions, sensitivity, review and
  export metadata, and per-file metadata.
- Source snapshot conformance checks pass for committed public examples.
- Private snapshots and all outputs generated from them remain private by
  default.
- Conformance checks remain bounded review aids, not safety certification.

### Microsoft 365 / SharePoint Proof Path

- The core repository includes the accepted
  [Microsoft 365 snapshot adapter boundary decision](../decisions/0001-microsoft-365-snapshot-adapter-boundary.md).
- The core repository includes a public-safe
  [synthetic SharePoint-style end-to-end demo](../demos/synthetic-sharepoint-end-to-end.md).
- Future provider-specific exporter behavior belongs in the
  [`agent-librarian-m365-snapshot-adapter`](https://github.com/ElvinMorales/agent-librarian-m365-snapshot-adapter)
  companion repository.
- v1.0 does not require a live Microsoft 365 connector to be ready in the core
  repository.
- Any live adapter must emit a compatible local source snapshot and satisfy its
  own permission, security, and release gates.

### Evals, Observability, and Conformance

- The full automated test suite passes.
- Package conformance passes.
- Source snapshot conformance passes for the committed synthetic fixture.
- Public-safety scans and checks remain bounded and their limitations remain
  documented.
- No private-source snapshots or generated outputs are committed.

## Compatibility Contract

v1.0 compatibility means consumers can rely on the documented purpose and
general structure of these surfaces. It does not freeze every field forever.
Additive fields may be introduced after v1.0 when documented and tested.

### CLI Commands

| Command | Stable purpose |
| --- | --- |
| `catalog` | Read a local artifact collection and write deterministic catalog outputs under the requested output directory. |
| `validate` | Validate generated catalog JSON against bundled schemas without modifying it. |
| `report` | Read generated outputs and print a human-review summary without modifying inputs. |
| `present` | Render generated catalog facts as an offline deterministic HTML overview by default. |

Command names and purposes above are stable. Options may be added. Changes to
existing option semantics, defaults, exit behavior, read scope, or write scope
must be documented and assessed for compatibility. Optional online behavior
must remain explicit and must not change the offline default.

### Generated Outputs

| File | Stable broad meaning |
| --- | --- |
| `index.json` | Machine-readable catalog entries and catalog-level metadata. |
| `catalog.md` | Human-readable catalog inventory and review information. |
| `overlap-report.json` | Deterministic duplicate and capability-overlap candidates for human review. |
| `diagnostics.json` | Per-file parse status, warnings, sanitized errors, and summary counts. |
| `overview.html` | Self-contained presentation of generated catalog facts. |
| `narrative.md` | Optional, labeled model-authored narrative used only when narration is explicitly requested. |
| `narrative-provenance.json` | Provenance for optional narration, including model, input identity, creation time, and token usage. |

The four catalog files remain the expected `catalog` outputs. `overview.html`
remains the default `present` output. The two narrative files are expected only
when optional narration exists and is requested. Additive fields and files are
permitted when documented and tested; removing an expected file or changing its
broad meaning requires breaking-change review.

### Source Snapshot Layout and Schema Version

A compatible source snapshot has this stable top-level shape:

```text
snapshot/
|-- source-manifest.json
`-- files/
```

`source-manifest.json` identifies its contract through `schema_version`. The
v1.0 release-prep candidate's bundled schema accepts `0.1.0`. A v1.0 release
must document the source manifest versions it accepts. A provider adapter must
emit one of those supported versions and pass the corresponding core
conformance check.

Additions that remain valid under a documented schema may be compatible.
Changing required fields, field meaning, path rules, sensitivity semantics, or
accepted schema versions requires explicit documentation, tests, a changelog
entry, and migration guidance when existing snapshots are affected. The core
repository owns this input-boundary compatibility contract; companion adapters
must follow it.

### Package Adapter Shape

The stable package organization is:

```text
agent/                    canonical, framework-neutral contract
packages/shared/          manifest schema and conformance expectations
packages/claude/          Claude package mappings, including Claude Code
packages/openai/codex/    Codex package mapping
packages/openai/gpt/      GPT advisory mapping
packages/openai/chatgpt-project/
                          ChatGPT Project advisory mapping
```

Platform-native filenames and required mappings are documented in
[`packages/README.md`](../../packages/README.md),
[`docs/portable-agent-packages.md`](../portable-agent-packages.md), and enforced
where applicable by `scripts/check_packages.py`. New files and mappings may be
added, but adapters must preserve the canonical source of truth, exact approval
rules for command-capable packages, advisory limits, sensitivity inheritance,
and human-review boundaries.

### Conformance Scripts

- `scripts/check_packages.py` verifies required adapter files, mappings, shared
  safety language, execution boundaries, and generated-output cleanliness.
- `scripts/check_source_snapshot.py` validates a local snapshot manifest and
  layout, path containment, listed file metadata and digests, and bounded
  leakage markers for public examples.

The scripts are stable, local validation entry points. Their checks may grow,
and new checks may cause previously unchecked defects to fail. A passing result
proves only that the documented bounded checks succeeded; it does not certify
safety, correctness, completeness, compliance, approval, publication
readiness, or production readiness.

## What May Change After v1.0

Compatible evolution may include:

- additive schema fields
- new diagnostics and warning codes
- new presentation sections
- new package adapter mappings
- new or stricter conformance checks
- new source snapshot provider patterns
- companion adapter improvements
- clearer documentation and synthetic examples

Every change still requires proportionate tests and documentation. The
changelog and, when consumers must act, migration guidance are required for:

- changed CLI options, defaults, or semantics
- changed generated output meanings
- changed schema requirements
- changed source manifest compatibility
- changed public/private safety boundaries

## Breaking-Change Policy

A change is breaking when it does any of the following:

- removes or renames a documented CLI command
- removes an expected generated output file without a compatible replacement
- changes schema or output meaning incompatibly
- weakens source snapshot scope, provenance, sensitivity, or review boundaries
- makes default CLI behavior require network access or provider credentials
- makes private snapshots or generated private outputs public by default
- removes labeling or provenance from narrated outputs

After v1.0, a breaking change requires a changelog entry, migration note,
compatibility rationale, and an explicit major/minor version decision based on
severity and the repository's adopted versioning policy. Safety-boundary
weakening must not be treated as a routine compatibility change merely because
it can be described in release notes.

## Public/Private Safety Contract

Public repository content must include no:

- secrets, credentials, tokens, or API keys
- real tenant IDs, account IDs, or SharePoint URLs
- real Microsoft 365 site, library, or folder names
- employer-specific examples or workflows
- regulated, client, patient, employee, or other private data
- private source snapshots
- generated catalogs, reports, or presentations from private snapshots
- unsanitized traces, logs, memory, runtime state, or access records
- raw provider responses or private source exports

Public examples are synthetic unless they have been explicitly reviewed,
sanitized, and approved for public use. Sanitization is a human-governed process
and is not established by a successful tool or conformance run.

Private/work source snapshots and generated outputs remain private by default.
v1.0 does not certify safety, correctness, completeness, compliance, approval,
publication readiness, or production readiness.

## Explicit Non-Goals for v1.0

v1.0 provides no:

- built-in live Microsoft 365 connector in the core repository
- Microsoft Graph or OAuth implementation in the core repository
- autonomous publication
- compliance certification
- private-data safety certification
- employer endorsement
- guarantee that generated catalogs are complete or correct without human
  review
- replacement for human review and approval
- permission to commit private snapshots or private generated outputs publicly

## v1.0 Release-Preparation Checklist

Issue [#100](https://github.com/ElvinMorales/agent-librarian/issues/100) may use
this checklist. Checking these items supports release preparation but does not
itself create or approve a release.

- [ ] Full automated tests pass.
- [ ] `python scripts/check_packages.py` passes.
- [ ] `python scripts/check_source_snapshot.py examples/source-snapshots/synthetic-team-space` passes.
- [ ] Synthetic catalog, validation, report, and offline presentation demos pass.
- [ ] The README front door accurately describes the v1.0 surfaces and boundaries.
- [ ] The changelog is updated for the intended release.
- [ ] The package version bump is prepared consistently in all authoritative locations.
- [ ] The release checklist is updated and reviewed.
- [ ] This compatibility contract is reviewed against the release candidate.
- [ ] No private data, source snapshots, or generated private outputs are committed.
- [ ] A maintainer manually reviews the release and tag language before either is published.

Release preparation must also verify that the actual release candidate, not
only this documentation branch, satisfies every readiness criterion above.

## Related Documentation

- [Public-Safe Adoption Guide](../adoption-guide.md)
- [External Source Snapshot Contract](../adapters/source-snapshot-contract.md)
- [Source Adapter Notes and Conformance Check](../adapters/README.md)
- [Synthetic SharePoint-Style End-to-End Demo](../demos/synthetic-sharepoint-end-to-end.md)
- [Claude Code Private-Source Snapshot Runbook](../demos/claude-code-private-source-snapshot.md)
- [Microsoft 365 Snapshot Adapter Boundary](../decisions/0001-microsoft-365-snapshot-adapter-boundary.md)
