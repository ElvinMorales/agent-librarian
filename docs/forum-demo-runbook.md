# Forum Demo Runbook

## Purpose

This runbook provides a public-safe, repeatable path for presenting
`agent-librarian` in an Agentic AI forum from a work computer. It keeps the
live demonstration focused on the committed synthetic sample collection and
the repository's inspectable artifact, validation, diagnostics, governance,
and review surfaces.

## Demo positioning

`agent-librarian` is a deterministic artifact-librarian reference
implementation for agentic AI systems. It demonstrates the artifact layer
around agents: identity, capabilities, tools, prompts, memory/state
boundaries, schemas, diagnostics, governance, review reports, and release
hygiene.

The demo should emphasize inspectable artifacts and bounded behavior rather
than model autonomy.

## What this demo is

- a local, deterministic cataloging and review workflow
- a reference implementation for agentic AI artifact infrastructure
- an example of treating selected Markdown, YAML, and JSON files as data
- a demonstration of generated catalogs, validation, diagnostics, warnings,
  overlap candidates, governance boundaries, and human review
- a public-safe workflow using only synthetic repository fixtures

## What this demo is not

It is not an autonomous LLM agent. It does not call an LLM, use the network,
execute scanned files, or make artifact-management decisions.

It is also not a hosted registry, semantic search system, automatic
deduplication engine, safety certification, or replacement for human review.

## Work-computer safety rules

- Clone only the public `ElvinMorales/agent-librarian` repository.
- Run catalog commands only against `examples/sample-collection`.
- Do not scan work folders.
- Do not scan internal documents.
- Do not scan Teams or SharePoint exports.
- Do not scan private prompts.
- Do not scan traces or logs.
- Do not scan credentials or secrets.
- Do not scan customer, user, regulated, or other private data.
- Do not imply employer sponsorship, approval, or endorsement.
- Keep the presentation limited to public repository files and synthetic
  committed outputs.

Local processing reduces exposure, but it does not make private material
appropriate for a public demonstration.

## Fresh clone setup

Use a new directory that contains no work material. In PowerShell:

```powershell
git clone https://github.com/ElvinMorales/agent-librarian.git
cd agent-librarian

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
agent-librarian --version
```

The clone and package installation require network access. The
`agent-librarian` commands in the live demo run locally and require no API key
or external service.

## Live demo command sequence

Run these commands from the repository root:

```powershell
agent-librarian catalog examples/sample-collection --out examples/generated-catalog
agent-librarian validate examples/generated-catalog
agent-librarian report examples/generated-catalog
```

Explain that `catalog` reads the synthetic artifacts as data and writes four
files under `examples/generated-catalog`. `validate` checks the generated JSON
against bundled schemas. `report` summarizes diagnostics, warnings, and
overlap candidates for human review without rescanning the source collection.

## Files to open during the demo

Open these files in this order as time allows:

1. `README.md`
2. `docs/showcase-brief.md`
3. `docs/demo-walkthrough.md`
4. `examples/generated-catalog/catalog.md`
5. `examples/generated-catalog/diagnostics.json`
6. `examples/generated-catalog/overlap-report.json`
7. `docs/taxonomy-architecture-map.md`
8. `docs/adoption-guide.md`

Start with `catalog.md` when showing generated output. Use `diagnostics.json`
to explain parse status and warnings, then use `overlap-report.json` to show a
deterministic candidate that still requires human judgment.

## 5-minute talk track

Agentic AI systems need more than prompts. They need artifacts: manifests,
skills, tool definitions, prompt interfaces, memory and state policies, output
schemas, diagnostics, safety guidance, tests, and release notes.

`agent-librarian` is a local deterministic reference implementation for
inspecting those artifacts. It treats files as data, catalogs them, validates
generated outputs, flags review conditions, and produces a human-review
report.

The point is not LLM autonomy. The point is the artifact and governance layer
agents need around them.

A practical five-minute sequence is:

1. Use the README and showcase brief to establish the problem and boundaries.
2. Run `catalog`, `validate`, and `report`.
3. Open `catalog.md` and show the readable artifact inventory.
4. Open diagnostics and overlap output to show bounded, explainable review
   signals.
5. Close with the taxonomy architecture map and the human-review boundary.

## If someone asks "is this really an agent?"

I would not call this an autonomous LLM agent. I would call it a deterministic
artifact-librarian agent or agentic infrastructure component. It has a bounded
role, explicit inputs and outputs, operating constraints, tool surfaces,
validation, diagnostics, and governance boundaries. I am showing it in an
agentic AI forum because these are the artifacts autonomous agents depend on
but often do not expose clearly.

## Fallback plan

- If Python setup fails, show the GitHub repository documentation and
  committed generated catalog files.
- If live commands fail, open the committed `examples/generated-catalog/`
  outputs.
- If time is short, show `docs/taxonomy-architecture-map.md` and the
  `agent-librarian report examples/generated-catalog` output.
- If asked about private use, point to `docs/adoption-guide.md`.

The presentation still works as a repository walkthrough because the sample
inputs and generated outputs are committed and intentionally public-safe.

## After the demo

- Do not replace the synthetic sample collection or committed outputs with
  work material.
- Do not share generated files from any private scan.
- Check `git status` before leaving the repository to confirm that only
  expected local demo changes exist.
- Deactivate the virtual environment with `deactivate` when finished.
- Direct follow-up questions about adapting the workflow to the public-safe
  adoption guide.

## Related docs

- [Project overview](../README.md)
- [Showcase brief](showcase-brief.md)
- [Demo walkthrough](demo-walkthrough.md)
- [Taxonomy-aligned architecture map](taxonomy-architecture-map.md)
- [Public-safe adoption guide](adoption-guide.md)
- [Public safety](public-safety.md)
- [Warnings and overlap](warnings-and-overlap.md)
