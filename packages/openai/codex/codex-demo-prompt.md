# Codex Demo Prompt

Use the `artifact-librarian` skill and the instructions in
`packages/openai/codex/AGENTS.md`.

Run the public-safe Agent Librarian demo only against:

```text
examples/sample-collection
examples/generated-catalog
```

First, explain the workflow in plain language. Then propose the runtime-wrapper
commands without running them. Show the exact command, read scope, write
scope, sensitivity warning, and what will not happen.

Demonstrate the wrong-approval failure:

```bash
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "wrong command"
```

Then ask for exact approval before running:

```bash
python -m agent_librarian.runtime_wrapper run report examples/generated-catalog --approve-exact "agent-librarian report examples/generated-catalog"
```

After execution, summarize only deterministic CLI evidence and generated
outputs. Do not certify safety, correctness, completeness, approval,
compliance, or publication readiness.

