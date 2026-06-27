# Presentation Demo Walkthrough

This walkthrough uses only the repository's synthetic catalog. The default
presentation is a deterministic offline rendering. The committed narrated
example is static demonstration output created with a local stub; it did not
contact Anthropic or any other provider.

## 1. Run the offline demo

From the repository root:

```bash
agent-librarian present examples/generated-catalog --out .tmp/present-demo
```

The same command works in PowerShell. It reads only `index.json`,
`diagnostics.json`, and `overlap-report.json`, then writes
`.tmp/present-demo/overview.html`. No API key, optional provider SDK, or network
connection is required.

## 2. Open the overview

In PowerShell:

```powershell
Start-Process .tmp/present-demo/overview.html
```

In common Linux desktop environments:

```bash
xdg-open .tmp/present-demo/overview.html
```

You can also open the file directly in a browser. The page has no external
CSS or JavaScript dependencies.

## 3. Review the artifact cards

Each card renders existing deterministic catalog fields: name, source path,
description, artifact type, taxonomy bucket, version, framework, owner,
extraction confidence, and discoverability warnings. Empty or weak metadata
should direct a reviewer back to the generated JSON and source artifact; the
card is not an independent source of truth.

## 4. Interpret diagnostics

The synthetic fixture reports six files: five `parsed`, one `partial`, and no
`failed` or `skipped` files. `partial` means useful metadata was extracted but
structure or important discoverability metadata was incomplete. It does not
mean the artifact is unsafe or unusable. Likewise, `parsed` is not a safety,
correctness, completeness, or publication-readiness certification.

## 5. Interpret overlap candidates

The overview shows one deterministic overlap candidate between the two
synthetic summarization skills. Its shared terms and confidence value are
evidence for human comparison, not a probability, duplicate verdict, merge
instruction, or automatic deduplication decision.

## 6. Compare the static narrated example

Open the committed examples:

- `examples/generated-presentation/overview.html` is the offline deterministic
  output.
- `examples/generated-presentation-narrated/overview.html` adds a static,
  synthetic narrative above the same deterministic facts.
- `examples/generated-presentation-narrated/narrative.md` contains that
  demonstration narrative.
- `examples/generated-presentation-narrated/narrative-provenance.json` shows
  the narrated-output provenance shape and identifies the local synthetic
  stub. Zero token counts confirm that this committed demo is not evidence of
  a live provider response.

A real narrated run is an explicit online action:

```bash
python -m pip install -e ".[narrate]"
export ANTHROPIC_API_KEY="..."
agent-librarian present examples/generated-catalog --out .tmp/present-narrated --narrate
```

PowerShell uses:

```powershell
python -m pip install -e ".[narrate]"
$env:ANTHROPIC_API_KEY = "..."
agent-librarian present examples/generated-catalog --out .tmp/present-narrated --narrate
```

Do not commit, print, or embed the API key. A real narrated run sends only the
three generated JSON documents to Anthropic, but those documents can contain
sensitive catalog metadata.

## 7. Keep narrative secondary

Model narrative can omit, misstate, or overemphasize information. Review the
deterministic artifact cards, diagnostics, overlap candidates, and underlying
JSON directly. Narrative is a review aid, not certification of safety,
privacy, correctness, completeness, compliance, approval, or publication
readiness.

## 8. Do not publish private presentations

Presentation outputs inherit source sensitivity. From private catalogs, do
not publish or commit `overview.html`, `narrative.md`, or
`narrative-provenance.json`. Narrative can repeat sensitive artifact names,
paths, warnings, and overlap information. Public demos must use synthetic
catalog data like the committed examples in this repository.

## v0.6 non-goals

The presentation layer does not provide source crawling, SharePoint or
Microsoft 365 connectors, MCP server behavior, multi-provider abstraction,
safety or compliance certification, publication approval, automatic
deduplication decisions, automatic artifact edits, or a private-to-public
sanitization guarantee.
