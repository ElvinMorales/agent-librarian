# Warnings and Overlap

`agent-librarian` emits deterministic warnings and overlap candidates to guide
human review. They are review aids, not severity-ranked policy findings. A
warning means an artifact may need attention before reuse or publication. It
does not automatically mean the artifact is unsafe, broken, or unusable.

There are no formal warning severity levels. Warning codes describe the kind of
review to perform, not a ranked level of risk.

## Warning Surfaces

Warnings can appear in these outputs:

- Catalog entry warnings are stored in `index.json` under
  `discoverability_warnings` and rendered in `catalog.md`.
- Diagnostics warnings are stored per file in `diagnostics.json`. For parsed
  entries, these include parser warnings and the entry warnings found before
  overlap analysis.
- Overlap findings are records in `overlap-report.json`. They also add
  `duplicate_candidate` or `overlap_candidate` to the affected catalog
  entries, but those two codes are not copied back into diagnostics.

A warning can appear on a diagnostic whose status is `parsed`. Status describes
the parse outcome; warnings can also request review without making extraction
partial or failed. In the current implementation, `overbroad_tool_scope` and
`public_safety_review_needed` do not by themselves change a diagnostic to
`partial`.

## Catalog Entry Warning Codes

| Warning code | Where it appears | Meaning | Suggested human review | It does not mean |
| --- | --- | --- | --- | --- |
| `missing_description` | Catalog entry and diagnostics | An agent, capability module, prompt template, tool manifest, or protocol manifest has no extracted description. | Add a concise description of what the artifact does and its intended use. | The file failed to parse or the artifact has no behavior. |
| `weak_description` | Catalog entry and diagnostics | The extracted description has fewer than five words or is `helper`, `useful tool`, or `does tasks` (case-insensitive). | Replace it with specific capability, scope, and outcome language. | The described capability is necessarily weak or incorrect. |
| `missing_activation_trigger` | Catalog entry and diagnostics | An agent, capability module, or prompt template has no extracted condition for when it should be used. | Document concrete activation conditions and important non-triggers. | The artifact can never be invoked or is always active. |
| `missing_inputs` | Catalog entry and diagnostics | An agent, capability module, or prompt template has no extracted input contract. | Document required and optional inputs, including expected formats. | The artifact accepts no input or cannot run. |
| `missing_outputs` | Catalog entry and diagnostics | An agent, capability module, or prompt template has no extracted outputs. | State the produced result, format, and required sections or fields. | The artifact produces no output or execution failed. |
| `missing_output_contract` | Catalog entry and diagnostics | No output contract was found. In the current implementation, this is emitted together with `missing_outputs`. | Define the output structure and constraints that consumers can rely on. | An existing output is known to violate a schema or contract. |
| `overbroad_tool_scope` | Catalog entry and diagnostics | Extracted tool scope contains `all tools`, `any tool`, or `*`. | Confirm the scope is intentional and replace it with the minimum named tools or capabilities needed. | The artifact has actually received unrestricted runtime access or has performed an unsafe action. |
| `side_effects_unclear` | Catalog entry and diagnostics | A capability module or tool manifest has no extracted side-effect statement. | State whether it reads, writes, sends, deletes, executes, or has no side effects. | Side effects definitely exist. |
| `missing_dependencies` | Catalog entry and diagnostics | An agent or capability module has no extracted dependencies. | List runtime, tool, data, protocol, and environment requirements, or explicitly state that there are none. | The artifact has unresolved installation dependencies. |
| `missing_examples` | Catalog entry and diagnostics | A capability module or prompt template has no extracted example section or field. | Add a small synthetic input/output or usage example. | The artifact has never been used or tested. |
| `missing_evals` | Catalog entry and diagnostics | An agent or capability module has no related-file reference containing `eval` or `test`. | Link relevant evaluations or tests, or document why none apply. | The artifact has failed evaluation or has no quality controls outside the scanned metadata. |
| `unknown_artifact_type` | Catalog entry and diagnostics | Classification rules did not recognize the file as a supported artifact type. | Confirm whether the file belongs in the collection and add metadata or naming that makes its role clear. | The file type is unsupported or its contents are invalid. |
| `public_safety_review_needed` | Catalog entry and diagnostics | Source text matched a conservative pattern for possible credential material, private endpoints, or runtime/private records. | Inspect the source before reuse or publication, remove private material, and follow the appropriate handling process. | Sensitive data is definitely present, or the artifact is safe after automated scanning. |
| `duplicate_candidate` | Catalog entry; represented by a `duplicate` candidate in the overlap report | A same-type pair reached the implemented duplicate-confidence threshold. | Compare purpose, triggers, inputs, outputs, and ownership before consolidating or cross-referencing. | The files are exact duplicates or one should be deleted. |
| `overlap_candidate` | Catalog entry; represented by a `capability_overlap` candidate in the overlap report | A same-type pair met the lower capability-overlap threshold. | Identify the shared capability and document intentional differences or opportunities to cross-reference. | The artifacts are interchangeable or should be merged. |

`public_safety_review_needed` can be accompanied by these
`public_safety_flags` values:

- `possible_credential_material`: terms resembling API keys, passwords,
  private keys, or bearer credentials were found.
- `possible_private_endpoint`: a localhost, loopback, or `.internal` HTTP(S)
  endpoint was found.
- `possible_runtime_record`: language associated with raw traces, live memory,
  runtime state snapshots, or real user data was found.

These flags are lexical matches. They identify material that needs human
inspection; they neither confirm nor rule out a disclosure.

## Diagnostics-Only Warning Codes

| Warning code | Where it appears | Meaning | Suggested human review | It does not mean |
| --- | --- | --- | --- | --- |
| `unsupported_file_type` | Diagnostics | The scanner inventoried a file whose suffix is not supported for parsing, so the file was skipped without reading its contents. | Decide whether to ignore, convert, or support the format in a separate change. | The file is unsafe, malformed, or unimportant. |
| `unterminated_frontmatter` | Diagnostics | A Markdown file starts a YAML frontmatter block but has no recognized closing delimiter. | Close or remove the frontmatter block, then regenerate the catalog. | The entire Markdown file is unreadable. |
| `non_mapping_frontmatter` | Diagnostics | Markdown frontmatter parsed successfully but its top-level YAML value is not a key-value mapping. | Convert the frontmatter to named fields such as `name`, `description`, and `tags`. | The YAML syntax is invalid. |
| `non_mapping_document` | Diagnostics | A YAML or JSON document parsed successfully but its top-level value is not an object/mapping. | Wrap catalog metadata in named top-level fields if the file is intended to describe an artifact. | The YAML or JSON syntax is invalid. |

Parse failures use the diagnostic `error` field and `failed` status rather than
a warning code.

## Overlap Scoring

Overlap analysis compares pairs only when both entries have the same artifact
type and that type is one of:

- `agent_definition`
- `agent_manifest`
- `capability_module`
- `prompt_template`
- `tool_manifest`

For each comparable pair, the tool derives normalized terms from the name,
description, purpose, tags, activation triggers, inputs, and outputs. Term
normalization lowercases text, removes configured stop words and short tokens,
and applies simple suffix stripping. The tool then calculates:

```text
confidence = 0.75 * all-field term similarity
           + 0.25 * name term similarity
```

Both similarities use Jaccard set similarity. The result is capped at `1.0`
and rounded to two decimal places before the reporting thresholds are applied.

`confidence` is deterministic heuristic similarity, not a probability,
quality score, or safety score. It is also separate from the extraction
confidence shown on catalog entries.

The implemented reporting bands are:

- `0.75` through `1.00`: reported as `duplicate`.
- `0.30` through `0.74`: reported as `capability_overlap` only when the pair
  also has at least three shared normalized terms.
- Below `0.30`, or fewer than three shared terms in the lower band: not
  reported.

`duplicate` means the pair crossed the higher heuristic threshold. It does not
mean the source files are byte-for-byte identical or semantically equivalent.

`capability_overlap` means the pair shares enough normalized vocabulary to
justify review, but did not cross the duplicate threshold. Different inputs,
outputs, activation triggers, constraints, or ownership can make both
artifacts useful.

Every reported candidate has `needs_human_review: true`. The tool does not
automatically merge, delete, rewrite, rank, or choose between artifacts.
Candidates are prompts for review, not decisions.

## Synthetic Examples

Two capability modules that both summarize meeting notes into the same
action-item format, with nearly identical triggers, inputs, and outputs, may be
reported as a `duplicate` candidate. A reviewer should still check whether
their constraints or intended audiences differ.

A research assistant and another agent definition focused on citation checking
may be reported as `capability_overlap` when both describe source review,
citations, and research outputs. They may not be duplicates if one produces a
full research brief while the other verifies claims in an existing draft.

## Safety and Correctness Limits

- Warnings do not certify safety.
- Schema validation confirms JSON structure; it does not certify semantic
  correctness.
- Absence of warnings does not mean an artifact is complete, safe, correct, or
  publication-ready.
- Public-safety review remains a human responsibility.
- Generated catalogs can expose names, paths, metadata, and review findings.
  Generated catalogs from private collections must not be committed.
