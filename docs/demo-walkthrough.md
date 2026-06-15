# Demo Walkthrough

## Purpose

This walkthrough supports a five-minute live demonstration of
`agent-librarian` from a clean checkout. It shows how the CLI catalogs the
repository's synthetic artifact collection, validates generated JSON
structure, and exposes diagnostics, warnings, and overlap candidates for
human review.

The project is a local, deterministic artifact-librarian reference
implementation. It does not call an LLM, execute scanned artifacts, or make
review decisions.

This walkthrough demonstrates the current CLI backend workflow. A future LLM
interaction layer could wrap the same bounded `catalog`, `validate`, and
`report` sequence by scoping intent, explaining safety boundaries, proposing a
command, requesting approval before execution, and summarizing the result.
The generated files, not the model summary, would remain the source of truth
for review.

## Demo boundaries

Use only these public, synthetic repository resources:

- the public `agent-librarian` repository
- `examples/sample-collection`
- `examples/generated-catalog`

Run all commands from the repository root. Do not substitute a personal,
private, employer, or production collection.

## Setup

Allow about one minute to install the package and confirm the CLI version:

```bash
python -m pip install -e ".[dev]"
agent-librarian --version
```

The demo is local and requires no API key or network service after
installation.

## Step 1: Inspect the synthetic sample collection

Open `examples/sample-collection` and point out the six fabricated artifacts:
an agent definition, a protocol manifest, a deliberately incomplete prompt,
two intentionally similar summarization skills, and a read-only tool
manifest.

The collection is small enough to inspect directly. The two summarization
skills provide a visible overlap case, while
`prompts/weekly-review.md` provides a visible incomplete-metadata case.

## Step 2: Generate the catalog

Allow about 30 seconds to run:

```bash
agent-librarian catalog examples/sample-collection --out examples/generated-catalog
```

The command scans supported files as data and writes only the four catalog
outputs under `examples/generated-catalog`. It does not import, source,
evaluate, or execute the sample artifacts.

Optional command variants:

```bash
agent-librarian catalog examples/sample-collection --out examples/generated-catalog --strict
agent-librarian catalog examples/sample-collection --out examples/generated-catalog --include "**/*.md"
agent-librarian catalog examples/sample-collection --out examples/generated-catalog --exclude "private,scratch,tmp"
```

Use `--strict` to exit non-zero when a selected file fails to parse. Include
patterns narrow the scan, and custom excludes add to the built-in safe
defaults. These controls support deliberate scope selection; they do not make
private inputs suitable for a public demo.

## Step 3: Validate generated outputs

Allow about 30 seconds to run:

```bash
agent-librarian validate examples/generated-catalog
```

Validation checks generated JSON structure. It does not certify semantic
correctness, safety, completeness, or publication readiness.

Optionally summarize the generated review surfaces before opening individual
files:

```bash
agent-librarian report examples/generated-catalog
```

The report reads the existing generated JSON files. It does not rescan the
sample collection or make review decisions.

## Step 4: Review the generated files

Open `examples/generated-catalog` and explain the four files:

- `index.json`: machine-readable catalog entries and generation metadata
- `catalog.md`: human-readable inventory with review warnings
- `overlap-report.json`: deterministic overlap candidates
- `diagnostics.json`: per-file parse status, warnings, and sanitized errors

Start with `catalog.md` for the readable inventory, then use the JSON files to
show the corresponding structured review surfaces.

## Step 5: Explain diagnostics, warnings, and overlap

Allow about one minute for three concrete findings in the committed outputs:

1. `diagnostics.json` records five parsed files and one partial file, with no
   failed files.
2. The synthetic weekly-review prompt is partial because it has a weak
   description and lacks outputs, an output contract, and an example.
3. `overlap-report.json` classifies the two summarization skills as a
   deterministic `duplicate` candidate that needs human review. This does not
   mean the files are byte-for-byte identical or semantically equivalent.

Parse status describes extraction results. Warnings identify metadata or
review conditions. Overlap confidence measures deterministic term similarity;
it is not a probability, quality score, or instruction to merge files.

## Step 6: Explain the human-review handoff

Allow about 30 seconds to show that the tool stops at inspectable evidence:

- reviewers compare the source artifacts with the generated entries
- reviewers decide whether warnings require documentation changes
- reviewers decide whether overlap is intentional, needs cross-referencing,
  or justifies consolidation
- reviewers inspect source files and generated outputs before publication

The CLI does not merge, delete, rank, approve, or publish artifacts. Warnings
and overlap candidates are review prompts, not decisions.

## Presenter notes

**What to say:** "This project is intentionally not calling an LLM. The point
of the current demo is to show the deterministic backend and artifact system
under a future interaction layer: files, schemas, generated outputs,
diagnostics, warnings, tests, and release boundaries."

**How to describe the future layer:** It may help a user scope intent, explain
boundaries, propose a documented CLI command, request approval, and summarize
outputs. It must not bypass the CLI, run arbitrary shell commands, invent
catalog findings, or certify artifacts as safe, complete, approved, or ready
to publish.

**Why local and deterministic matters:** Review findings come from explainable
rules rather than a remote model. CI fixes `SOURCE_DATE_EPOCH` when
byte-for-byte reproducible generated files are required.

**Why warnings are prompts:** A warning makes missing or potentially risky
metadata visible. It does not prove that an artifact is broken, unsafe, or
ready for a particular action.

**Why review generated catalogs:** Catalogs can expose names, paths, metadata,
and review findings. Structural validation cannot determine whether that
context is appropriate to publish.

**Why use synthetic examples:** The committed collection demonstrates partial
metadata and overlap without exposing private prompts, operational records,
user data, or employer-specific workflows.

## What not to demo publicly

Public demos must use only the public repository,
`examples/sample-collection`, and `examples/generated-catalog`.

Do not demo:

- private collections
- employer workflows
- internal repositories
- private prompts
- real traces
- memory or state snapshots
- credentials or secrets
- regulated or private data
- generated catalogs from non-public sources

Local processing reduces exposure, but it does not make arbitrary source
material safe to publish. Review both source artifacts and generated outputs
before any public use.

## Related docs

See the [taxonomy-aligned architecture map](taxonomy-architecture-map.md) for
the connection between this demo flow, the repository's implementation
artifacts, generated outputs, governance surfaces, and all 14 taxonomy buckets.

Before adapting the workflow to another collection, read the
[public-safe adoption guide](adoption-guide.md).
