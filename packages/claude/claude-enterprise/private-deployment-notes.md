# Private Deployment Notes

These notes describe a public-safe adaptation path for private Claude
Enterprise deployments. They intentionally avoid employer-specific examples,
private URLs, private prompts, traces, logs, memory snapshots, and state
snapshots.

## Public Package vs Private Adaptation

The public package demonstrates the workflow with synthetic fixtures. A
private deployment may adapt the same contract to authorized internal
collections, but private source material and derived outputs stay inside the
private environment.

Use placeholders in public docs:

```text
PRIVATE_SOURCE
PRIVATE_OUTPUT
PRIVATE_CATALOG
```

Do not replace those placeholders with real private paths in committed
package files.

## Private Handling

Private deployments should define:

- who may request a scan
- who may approve exact commands
- where generated outputs are stored
- who may review outputs
- how long outputs and approval logs are retained
- how private generated outputs are deleted
- when separate publication or sharing review is required

Generated catalogs, reports, approval logs, execution records, and summaries
inherit source sensitivity.

## Runtime Limits

This package does not provide a Claude API integration, network bridge,
MCP server, hosted service, or arbitrary shell executor. Any such exposure
requires separate design, security, privacy, and operational review.

Private deployments should keep the deterministic CLI backend and exact
approval wrapper as the enforcement boundary unless a replacement boundary is
explicitly reviewed.

