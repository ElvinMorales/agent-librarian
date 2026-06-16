# Claude Code Install Notes

These notes prepare a local Claude Code workspace for the public-safe
`agent-librarian` demo. They do not install a Claude API integration and do
not add network behavior.

## From a Tagged Release

1. Check out the desired release tag or unpack the release source archive.
2. Install the project locally:

   ```bash
   python -m pip install -e ".[dev]"
   ```

3. Copy `packages/claude/CLAUDE.md` to the repository root as `CLAUDE.md` if
   Claude Code expects project instructions at the workspace root.
4. Copy or reference the skill directory:

   ```text
   packages/claude/claude-code/.claude/skills/artifact-librarian-demo
   ```

5. Open the repository in Claude Code and invoke the skill with
   `packages/claude/claude-code/demo-prompt.md`.

## From the Current Checkout

1. Stay in the repository root.
2. Install the project locally:

   ```bash
   python -m pip install -e ".[dev]"
   ```

3. Tell Claude Code to use `packages/claude/CLAUDE.md` as project
   instructions or copy it to root `CLAUDE.md` for the demo.
4. Use the packaged skill from:

   ```text
   packages/claude/claude-code/.claude/skills/artifact-librarian-demo/SKILL.md
   ```

## Demo Scope

The public demo uses only:

```text
examples/sample-collection
examples/generated-catalog
```

Do not scan private or work-internal folders. Do not include internal URLs,
credentials, secrets, private prompts, private traces, logs, memory snapshots,
state snapshots, or private generated catalogs.

