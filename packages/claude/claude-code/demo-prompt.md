# Claude Code Demo Prompt

Use the `artifact-librarian-demo` skill and the project instructions in
`packages/claude/CLAUDE.md`.

Run a public-safe demo of `agent-librarian` using only the synthetic
`examples/sample-collection` and existing `examples/generated-catalog`.

Please:

1. Explain the safe scope in plain language.
2. Propose the wrapper commands before running anything.
3. Demonstrate the wrong approval failure.
4. Ask for exact approval before the correct wrapper `run`.
5. Run only the approved wrapper command.
6. Summarize the deterministic CLI evidence.
7. Point me to the generated files a human should review.
8. Explain what the demo proves and what it does not prove.

Do not scan outside the synthetic example scope. Do not run arbitrary shell.
Do not commit, push, tag, release, or open a pull request.

