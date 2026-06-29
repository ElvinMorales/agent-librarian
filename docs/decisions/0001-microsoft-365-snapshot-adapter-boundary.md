# Decision 0001: Microsoft 365 Snapshot Adapter Boundary

- Status: Accepted
- Date: 2026-06-29
- Issue: [#96](https://github.com/ElvinMorales/agent-librarian/issues/96)

## Context

`agent-librarian` is a deterministic, local-first CLI. Its catalog, validate,
report, and default presentation paths operate on local files. The source
snapshot contract preserves that boundary by requiring an external system to
be represented as a local, reviewable snapshot before cataloging.

A Microsoft 365 / SharePoint exporter would introduce provider-specific
authentication, authorization, API behavior, tenant scope, dependencies, and
operational risk. Placing that behavior in the core package would weaken its
provider-neutral local boundary. The repository therefore needs an explicit
ownership and permission decision before connector work begins.

## Decision

Any future live Microsoft 365 / SharePoint snapshot adapter will live in a
separate companion repository, tentatively named
`agent-librarian-m365-snapshot-adapter`. Live provider integration does not
belong in the core `agent-librarian` repository at this time.

The core repository owns:

- local catalog, validate, report, and present behavior
- the source snapshot contract and source manifest schema
- offline source snapshot conformance checks
- synthetic examples and public-safe documentation
- compatibility expectations and versioning guidance for snapshot inputs

The companion adapter repository owns:

- provider-specific setup and operating documentation
- Microsoft Graph and OAuth implementation, if separately approved
- export logic constrained to a pre-approved scope
- writing local snapshot files and generating compatible source manifests
- adapter-specific tests and mocked provider interactions

The adapter's output is the integration boundary. It must produce a local
snapshot compatible with the core repository's documented contract and bundled
manifest schema. It must not make the core scanner authenticate, call Microsoft
Graph, crawl a remote source, or depend on Microsoft-specific packages.

This decision does not approve or implement an exporter. It establishes the
repository boundary and the minimum safety conditions for future work.

## Permission model

Any future adapter must enforce all of these constraints:

- source access is read-only
- the site, library, and folder scope is explicit and approved before a run
- allowed file extensions and excluded paths are explicit
- traversal stops at the approved depth or equivalent boundary
- broad tenant discovery or crawling is prohibited
- access outside the approved scope is prohibited
- write, move, delete, upload, rename, permission-change, and sharing
  operations are prohibited
- output is written only to a local snapshot destination
- credentials, auth tokens, secret-bearing API responses, raw logs, traces,
  private memory or state, and unrelated workspace content are never collected
  into the snapshot or manifest
- generated catalogs, reports, and presentations inherit source sensitivity

The narrow approved scope, not the identity's maximum available privileges,
defines what a run may access. A technically over-privileged identity does not
authorize broader collection and must fail the security review described below.

## Approved scope model

Before access, a future adapter configuration must require the following
conceptual fields. Its run manifest must preserve the effective values using
the existing source manifest schema. Public documentation and fixtures must use
only fabricated placeholders such as `<TENANT_OR_PROVIDER>`, `<SITE>`, and
`<LIBRARY>`.

| Required field | Purpose and manifest mapping |
|---|---|
| `source_system` | Provider type and display placeholder under `source_system`. |
| `tenant_or_provider_placeholder` | Non-secret placeholder represented by `source_system.name`, `provider_hint`, or `source_locator`; never a real public fixture value. |
| `site_placeholder` | Approved site boundary, represented in the approved-scope description or included roots. |
| `library_placeholder` | Approved library boundary, represented in the approved-scope description or included roots. |
| `folder_scope` | Narrow included roots under `approved_scope.included_roots`. |
| `allowed_extensions` | Explicit allowlist under `approved_scope.allowed_extensions`. |
| `excluded_paths` | Excluded roots and per-path reasons under `approved_scope.excluded_roots` and `excluded_paths`. |
| `max_depth` or traversal boundary | `approved_scope.max_depth`, or an equally explicit bounded traversal rule recorded in scope notes. |
| `exported_at` | Run timestamp under `export.exported_at`. |
| `review_owner` | Accountable reviewer under `review.review_owner`. |
| `approval_note` | Approval context under approved-scope or review notes. |
| `sensitivity` | Snapshot and output handling rules under `sensitivity`. |

The run manifest must also record `export.source_access_read_only: true` and the
exported file metadata required by the current schema. Configuration must be
validated before remote access. The adapter must fail closed when required
scope is missing, ambiguous, or broader than the approved boundary.

## Public-safe synthetic demo requirements

Future issue #98 must remain independent of a live Microsoft 365 tenant. Its
demo must:

- use only a fabricated SharePoint-like source snapshot
- use no live tenant, credentials, or network access
- include a source manifest compatible with the existing schema
- use local commands only
- derive any committed catalog, report, or presentation solely from synthetic
  files
- state that the demo does not prove live connector readiness
- exclude real exports, tenant or account IDs, internal URLs, screenshots,
  employer examples, private document names, and work-derived outputs

## Security and review gate for exporter work

Issue #97 may start only in the companion repository and only after this
decision is merged. Before implementation, that repository must document and
approve:

- a threat model or equivalent safety checklist
- the authentication and least-privilege permission design
- configuration, credential, token, and secret handling
- a test strategy based on mocks and stubs, with no live API calls in CI
- a policy separating synthetic public examples from private local snapshots
- `.gitignore` rules and operator guidance for local credentials, snapshots,
  logs, caches, and generated outputs
- a release boundary stating that the adapter is optional, provider-specific,
  separately versioned, and not part of the core package

Review must also verify the explicit operation allowlist, fail-closed scope
validation, redaction-safe errors, local output handling, manifest compatibility,
and the absence of telemetry or diagnostic payloads that could capture private
content. A live-tenant test, if ever authorized, must remain outside public CI
and outside this core repository.

## Consequences

Benefits:

- the core repository stays local-first, framework-neutral, and
  provider-neutral
- Microsoft-specific dependencies and authentication code stay out of the core
  package
- accidental connector behavior cannot enter the core CLI through this work
- public core artifacts and private adapter operations have a clearer boundary
- the adapter can evolve and release independently

Costs:

- users must understand two repositories
- the adapter and source manifest schema need explicit compatibility management
- setup, versioning, and troubleshooting require cross-repository documentation

## Follow-up tasks

- #97 may proceed only after this decision is merged and must target the
  companion repository under the gates above.
- #98 must remain synthetic and must run without a live Microsoft 365 tenant.
- Reconsidering the repository boundary requires a new decision record; it is
  not implied by future schema or documentation changes.
