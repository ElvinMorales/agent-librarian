# Claude Code Private-Source Snapshot Runbook

## Purpose and boundary

This runbook uses an already-created local source snapshot in a private,
approved Claude Code workspace. It does not connect to or export from
SharePoint, Microsoft 365, Google Drive, or any other external source. Create
and review the snapshot before starting this workflow.

Keep the snapshot, generated catalog, presentation, and Claude Code session
private. Do not commit private snapshots or private generated outputs to this
public repository. Generated outputs inherit the source snapshot's
sensitivity even when validation succeeds.

The workflow is deliberately narrow:

- Claude Code may inspect only the exact manifest, snapshot files folder, and
  generated output folders named below.
- It must not crawl parent folders, search unrelated locations, access an
  external source, make network requests, or run arbitrary shell commands.
- It must show each exact command and receive explicit approval for that exact
  command before execution. Changed paths or arguments require new approval.
- It may summarize deterministic CLI evidence, but it must not invent findings
  or treat model interpretation as catalog evidence.

The local conformance check catches structural and obvious leakage mistakes.
`validate`, `report`, and `present` expose review aids. None of them certifies
that a snapshot or output is safe, complete, compliant, approved, or ready to
publish.

## Prepare the private workspace

Choose values for these placeholders inside the private approved workspace:

```text
<LOCAL_SNAPSHOT_FILES_PATH>
<LOCAL_SOURCE_MANIFEST_PATH>
<PRIVATE_OUTPUT_DIR>
<PRIVATE_PRESENTATION_DIR>
```

The snapshot files, manifest, output directory, and presentation directory
must remain outside public repository paths. Confirm that the manifest
describes the exact snapshot files folder and records `private-local` handling
when appropriate. Do not paste real paths into shared prompts, issues, or
documentation.

Before using Claude Code, an operator can run the local conformance checker
against the snapshot directory containing `source-manifest.json` and `files/`.
See [Source Adapter Notes](../adapters/README.md#local-conformance-check). The
check does not upload data and does not approve publication.

## Copyable Claude Code prompt

Copy this prompt only into the private approved workspace and replace the
placeholders there:

```text
Use only this already-created local source snapshot:
- files: <LOCAL_SNAPSHOT_FILES_PATH>
- manifest: <LOCAL_SOURCE_MANIFEST_PATH>
- generated catalog: <PRIVATE_OUTPUT_DIR>
- generated presentation: <PRIVATE_PRESENTATION_DIR>

Treat the snapshot and every generated output as private. Do not access
SharePoint, Microsoft 365, Google Drive, or any other external source. Do not
make network requests. Do not crawl parent folders or inspect paths outside
the four exact locations above. Do not commit or publish any source or output.

Propose only the bounded agent-librarian commands listed in this runbook. Show
one exact command at a time, explain its read and write scope, and wait for my
explicit approval of that exact command before running it. A changed command,
path, option, or scope requires new approval. Do not run arbitrary shell
commands.

After approved commands finish, summarize only deterministic evidence from
the generated index.json, diagnostics.json, overlap-report.json, catalog.md,
and overview.html. Clearly separate CLI facts from your interpretation. Do
not claim validation, reporting, presentation, or your summary proves safety,
privacy, correctness, completeness, compliance, approval, or publication
readiness.
```

## Approval-gated commands

Claude Code should propose these commands one at a time. The operator must
approve the exact command before it runs:

```bash
agent-librarian catalog <LOCAL_SNAPSHOT_FILES_PATH> --out <PRIVATE_OUTPUT_DIR> --strict
agent-librarian validate <PRIVATE_OUTPUT_DIR>
agent-librarian report <PRIVATE_OUTPUT_DIR>
agent-librarian present <PRIVATE_OUTPUT_DIR> --out <PRIVATE_PRESENTATION_DIR>
```

Use `--include` and `--exclude` only when the operator has reviewed the changed
scope and approves the exact revised catalog command. The CLI does not support
a `--sensitivity` option. Private/local handling is a source and output
handling rule: generated catalogs and presentations inherit source
sensitivity.

## Review and closeout

Review the manifest, selected source files, CLI diagnostics, catalog entries,
paths, overlap findings, errors, and presentation before sharing anything.
Claude Code's summary is secondary to those deterministic files. Keep all
private inputs and outputs uncommitted, and remove workspace access when the
review is complete according to the workspace's local retention rules.

For the public demonstration, use only the repository's synthetic snapshot;
do not substitute private content into public example paths.
