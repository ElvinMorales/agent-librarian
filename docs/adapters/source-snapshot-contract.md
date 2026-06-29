# External Source Snapshot Contract

`agent-librarian` catalogs local files. External systems such as document
libraries, shared drives, or collaboration workspaces should become local,
reviewable source snapshots before the CLI scans them.

This contract defines the design-time boundary for that workflow. It does not
add a connector, network behavior, authentication flow, or provider integration.

## Purpose

A source snapshot is a local folder plus provenance metadata that records:

- what external source was represented
- what scope was approved
- what files were exported
- what paths were intentionally excluded
- what sensitivity rules apply to the snapshot and generated outputs
- who must review the result before reuse or publication

The goal is to keep external-source handling inspectable without changing the
deterministic CLI backend.

## Snapshot-first architecture

```text
external source
  -> approved read-only export or sync
  -> local source snapshot
  -> source manifest
  -> agent-librarian catalog / validate / report / present
  -> human review
```

The CLI should only see the local source snapshot. It should not authenticate to
the external system, crawl remote locations, or decide whether the source is safe
to publish.

## Roles

| Role | Responsibility |
|---|---|
| Source system | The external system represented by the snapshot. |
| Approved scope | The narrow set of folders, extensions, and exclusions approved before export. |
| Source adapter | Any external process or tool that creates the local snapshot. It stays outside the core scanner. |
| Local snapshot | The local folder copied or exported from the approved scope. |
| Source manifest | The provenance and review metadata for the local snapshot. |
| Generated catalog | The deterministic `agent-librarian` outputs derived from the local snapshot. |
| Human reviewer | The person responsible for checking sensitivity, scope, warnings, and reuse/publication readiness. |

## Required manifest metadata

A source manifest should include:

- `schema_version`
- `source_snapshot_id`
- source system type, name, provider hint, and placeholder/source locator
- approved scope description, approver, timestamp, included roots, excluded roots,
  allowed extensions, and depth limit
- local snapshot root, creator, read-only flag, and catalog-ready flag
- export timestamp, method, tool name, and tool version
- exported file list with snapshot path, source path, media type, size, digest,
  last modified timestamp, classification, and notes
- excluded paths with reasons
- sensitivity level and whether snapshot/generated outputs may be committed
- review owner, review status, and review notes

The bundled schema is:

```text
src/agent_librarian/schema_data/source-manifest.schema.json
```

A synthetic example is:

```text
examples/source-snapshots/synthetic-team-space/source-manifest.json
```

## Source adapter boundary

A source adapter may:

- export or sync an approved external scope into a local folder
- produce a source manifest
- record file digests and timestamps
- preserve enough provenance for human review

A source adapter must not require changes to the deterministic scanner. It should
not cause `catalog`, `validate`, `report`, or default `present` to call external
services.

## Catalog boundary

`agent-librarian` may catalog the local snapshot after it exists. The CLI should:

- read the local files as data
- apply the same include and exclude behavior as other local collections
- write generated outputs under the requested `--out` directory
- keep deterministic facts as the source of truth

The generated outputs inherit the source snapshot sensitivity. A private source
snapshot produces private generated outputs unless a human review explicitly
sanitizes and approves a public version.

## Public-safety rules

Do not commit real source snapshots or generated catalogs from private systems to
this public repo.

Public examples must use synthetic data. Do not include:

- real tenant names, site names, library names, private paths, or internal URLs
- employer-specific workflows
- regulated, client, patient, employee, or personal data
- screenshots from private systems
- secrets, credentials, tokens, API keys, account IDs, or access logs
- raw traces, memory stores, runtime state, or workspace snapshots

A source manifest is provenance for a local snapshot. It is not proof that the
snapshot is complete, safe, compliant, approved, or publishable.

## Minimal review checklist

Before cataloging a snapshot:

- [ ] The approved scope is narrow and documented.
- [ ] Excluded roots cover private, people, raw export, archive, credential, and
      draft locations as appropriate.
- [ ] Allowed extensions are explicit.
- [ ] The local snapshot contains only intended files.
- [ ] The source manifest validates against the schema.
- [ ] The reviewer understands that generated outputs inherit sensitivity.

Before publishing anything derived from a snapshot:

- [ ] The snapshot is synthetic or has been sanitized for public use.
- [ ] Generated outputs were reviewed by a human.
- [ ] No private source paths, names, comments, screenshots, IDs, or endpoints are
      present.
- [ ] Warnings and overlap candidates are treated as review prompts, not approval.
- [ ] The public artifact explains what is intentionally not included.
