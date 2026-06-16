# Future Actions Notes

Future GPT Actions or API wrappers are out of scope for this package.

This advisory package does not add OpenAI API integration, network behavior,
MCP server code, arbitrary shell execution, local filesystem access, CLI
runtime changes, deterministic schema changes, generated-output changes, or a
package version bump.

If a future Action/API wrapper is proposed, it must be designed and reviewed
as a new execution surface. It must preserve the canonical contract:

- only documented `catalog`, `validate`, and `report` actions
- no arbitrary shell
- no source execution or modification
- exact approval for the visible command and scope
- generated outputs inherit source sensitivity
- CLI-generated files and command output remain the source of truth
- validation and reports remain review aids, not certifications
- no claim of safety, privacy, correctness, completeness, approval,
  compliance, or publication readiness

Until such a wrapper exists, GPT is advisory and should ask the user to run
deterministic commands locally when evidence is missing.

