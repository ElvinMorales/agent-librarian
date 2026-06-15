# State Strategy

The current deterministic CLI is stateless between commands. In-memory entries,
diagnostics, and overlap candidates exist only for the duration of one process.

The selected CLI output directory is explicit run output. Generated
`index.json`, `catalog.md`, `diagnostics.json`, and `overlap-report.json` files
are review artifacts, not hidden session state, durable memory, or resumable
runtime checkpoints.

For a future LLM runtime:

- Proposed scope and command approval must be explicit and visible.
- Approval applies only to the command and scope shown to the user.
- Any approval log, run record, execution result, or summary state must be an
  explicit, inspectable artifact with a defined retention policy.
- Hidden state must not change scan scope, expand permissions, imply approval,
  or affect publication decisions.
- A later run must not inherit approval from a prior conversation or run.
- State associated with private sources or generated catalogs is private by
  default.

The public repository must not contain real run state, session snapshots,
pending approvals, tool-call histories, private paths, or private generated
outputs. Use synthetic examples only if future state artifacts are added.
