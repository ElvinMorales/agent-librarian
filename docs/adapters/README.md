# Source Adapter Notes

This folder documents the source snapshot boundary for future external-source
work. The deterministic `agent-librarian` CLI still catalogs local files only.

Start here:

- [External Source Snapshot Contract](source-snapshot-contract.md)
- [SharePoint Snapshot Pattern](sharepoint-snapshot-pattern.md)

The source snapshot contract belongs to the design-time artifact layer. It helps
future adapters represent external systems as local, reviewable snapshots before
cataloging. It does not add live connector code, authentication, provider
configuration, or network behavior.

Public examples must stay synthetic. Real private snapshots and generated
catalogs should remain private unless reviewed and sanitized.
