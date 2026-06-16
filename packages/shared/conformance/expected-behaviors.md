# Expected Behaviors

Future package adapters must preserve these shared behaviors.

## Source and Package Relationship

- Treat `agent/` as the canonical source of truth.
- Treat `packages/` files as adapters for host-specific file formats.
- Do not introduce platform-specific policies that weaken canonical safety,
  approval, or evidence rules.
- Use only synthetic/public-safe examples in committed package files.

## Command Behavior

- Propose only documented commands:
  - `agent-librarian catalog SOURCE_DIR --out OUTPUT_DIR`
  - `agent-librarian validate CATALOG_DIR`
  - `agent-librarian report CATALOG_DIR`
- For `catalog`, expose any `--include`, `--exclude`, or `--strict` arguments
  in the exact proposal.
- Do not run arbitrary shell, chained commands, source files, deletion,
  editing, merging, publication, or provider/network actions.
- Command-capable adapters may execute only when the host provides local tools
  and the exact approval gate passes.
- Advisory adapters must provide review guidance and suggested commands only.

## Approval Behavior

- Show the exact command before execution.
- Show exact source, output, or catalog path.
- Show expected reads, expected writes, and generated files.
- Explain that source files are treated as data and are not executed,
  modified, merged, deleted, or published.
- Require exact approval for the visible command and scope.
- Require fresh approval for any changed command, path, optional argument,
  sensitivity class, retry, or publication request.

## Evidence Behavior

- Treat CLI-generated files and command output as source-of-truth evidence.
- Treat validation and reports as review aids, not certifications.
- Treat model-authored summaries as secondary aids.
- Do not invent missing files, counts, warnings, validation status, report
  findings, or overlap candidates.
- Preserve parse failures, warnings, diagnostics, and partial status.

## Safety Behavior

- Treat unclear sensitivity as private until clarified.
- Warn that private generated outputs inherit source sensitivity.
- Refuse public use of work, client, customer, regulated, trace, log, memory,
  state, or other private-derived material.
- Refuse safety, privacy, correctness, completeness, compliance, approval, or
  publication-readiness certification.
- Require separate human review before sharing or publication.

