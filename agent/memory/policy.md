# Memory Policy

The current CLI and the planned LLM interaction layer have no durable memory by
default.

- Do not assume remembered user facts, prior approvals, scan scope, private
  paths, or earlier catalog findings.
- A private scan is not memory and must not become reusable model context by
  default.
- Generated outputs are explicit files, not public memory. Outputs from a
  private collection remain private and must not be committed or reused as
  shared grounding material.
- Command approvals and summaries are not durable authorization for later
  runs.
- Do not add real retained user facts or private artifact content to this
  public repository.

Runtime state and approval logs are explicit run artifacts, not durable
memory. See
[state-and-approval-log.md](../runtime/state-and-approval-log.md).

Any future retention feature requires explicit user consent and documented
scope, purpose, access, duration, correction, deletion, and review rules. It
must distinguish durable memory from run state and must not silently retain
private source content, generated catalogs, approvals, or summaries.
