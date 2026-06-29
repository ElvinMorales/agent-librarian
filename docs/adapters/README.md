# Source Adapter Notes

This folder documents the source snapshot boundary for future external-source
work. The deterministic `agent-librarian` CLI still catalogs local files only.

Start here:

- [External Source Snapshot Contract](source-snapshot-contract.md)
- [SharePoint Snapshot Pattern](sharepoint-snapshot-pattern.md)
- [Microsoft 365 Snapshot Adapter Boundary](../decisions/0001-microsoft-365-snapshot-adapter-boundary.md)
- [Synthetic SharePoint-Style End-to-End Demo](../demos/synthetic-sharepoint-end-to-end.md)
- [Claude Code Private-Source Snapshot Runbook](../demos/claude-code-private-source-snapshot.md)

## Local conformance check

From the repository root, check a snapshot directory containing
`source-manifest.json` and `files/`:

```bash
python scripts/check_source_snapshot.py examples/source-snapshots/synthetic-team-space
```

The check is local and makes no network calls. It validates the manifest
against the bundled source manifest schema, verifies that manifest file paths
stay under `files/`, checks listed file existence, size, and SHA-256 digests,
reports unlisted files, and scans public/public-synthetic snapshots for
targeted obvious leakage markers. Private-local snapshots receive structural
and digest checks without applying the public-example marker policy.

A passing check means only that these bounded checks succeeded. It does not
certify safety, privacy, completeness, compliance, approval, or publication
readiness. Human review of both source and generated outputs remains required.

The source snapshot contract belongs to the design-time artifact layer. It helps
future adapters represent external systems as local, reviewable snapshots before
cataloging. It does not add live connector code, authentication, provider
configuration, or network behavior.

Public examples must stay synthetic. Real private snapshots and generated
catalogs should remain private unless reviewed and sanitized.
