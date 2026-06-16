# Codex Validation Checklist

Use this checklist before treating the Codex package as aligned with the
shared package contract.

- `packages/openai/codex/AGENTS.md` says Codex is the interface layer and the
  deterministic CLI/generated outputs are the source of truth.
- The package uses only `examples/sample-collection` and
  `examples/generated-catalog` for public demos.
- Runtime-wrapper `propose` is preferred before `run`.
- Wrapper `run` requires exact approval for the visible command and scope.
- The wrong-approval command is documented as a nonzero failure that must not
  execute the deterministic backend.
- The package refuses private/work scans for public demos, arbitrary shell,
  source execution, source modification, commits, pushes, tags, releases, pull
  requests, and GitHub/yeet publishing flows unless explicitly requested where
  applicable.
- Summaries are bounded by deterministic generated outputs and command output.
- The package does not certify safety, correctness, completeness, approval,
  compliance, or publication readiness.
- The package does not add OpenAI API integration, network behavior, MCP
  server code, CLI/runtime behavior, deterministic schema changes, generated
  output changes, or a package version bump.

