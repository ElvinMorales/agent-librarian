# SharePoint Snapshot Pattern

This pattern describes how a Microsoft 365 / SharePoint-style source can be
represented as a local source snapshot before `agent-librarian` catalogs it.

This is documentation only. It does not add Microsoft Graph code, OAuth setup,
tenant configuration, live connector behavior, or network access.

## Safe architecture

```text
SharePoint / Microsoft 365 source
  -> approved read-only export or sync
  -> local source snapshot + source-manifest.json
  -> agent-librarian catalog
  -> validate / report / present
  -> human review
```

The important boundary is that SharePoint is not the scanner. SharePoint is the
source. The scanner only receives local files that were already exported into an
approved snapshot folder.

## Approved scope checklist

Before creating a snapshot, define:

- approved source system or workspace
- approved site, library, folder, or saved export scope
- allowed file extensions
- excluded folders and patterns
- maximum depth, if useful
- review owner
- sensitivity level
- whether the local snapshot may be cataloged
- whether the generated outputs may be committed, shared, or must remain private

Use placeholder values in public docs and examples.

## Suggested local layout

```text
source-snapshot/
├── source-manifest.json
└── files/
    ├── Policies/
    │   └── public-safety-notes.md
    └── Prompts/
        └── catalog-review-prompt.md
```

The `files/` folder is the catalog input. The manifest is the provenance record.
The manifest is not a remote connection configuration and is not cataloged as
part of `files/`.
Generated outputs should go somewhere separate, such as `.tmp/source-catalog/` or
another private output folder.

Example local command:

```bash
agent-librarian catalog source-snapshot/files --out .tmp/source-catalog --strict
agent-librarian validate .tmp/source-catalog
agent-librarian report .tmp/source-catalog
```

## What to exclude

For a real private source, exclude anything outside the approved review scope,
especially:

- people directories
- HR, finance, legal, clinical, regulated, or client-specific locations
- private notes, drafts, raw exports, archive dumps, and chat transcripts
- access logs, trace logs, memory/state folders, runtime records, and screenshots
- credentials, secrets, tokens, environment files, and configuration exports

The public repo should contain only synthetic examples.

## Claude Code private-source demo note

For a private demo in an approved local workspace, Claude Code should receive
only the local snapshot path and the public-safe instructions needed to run the
deterministic CLI. The private source itself should stay local.

A safe internal prompt shape is:

```text
Use the local snapshot at <LOCAL_SNAPSHOT_FILES_PATH>.
Do not access external systems.
Do not publish generated outputs.
Run only documented agent-librarian commands.
Treat all generated outputs as private-local unless I explicitly say otherwise.
Summarize warnings, diagnostics, and overlap candidates for human review.
```

This keeps the private source workflow separate from public repo artifacts.

## Review reminders

- A source manifest is not a safety certificate.
- Generated catalogs inherit the source snapshot sensitivity.
- `validate` checks JSON shape, not privacy or completeness.
- `report` summarizes review surfaces, not final decisions.
- `present` renders generated facts; optional narration is a secondary review aid,
  not approval.
- Public examples must be synthetic.
