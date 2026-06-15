# Forum Feedback Log

## Purpose

This log captures comments, questions, objections, and ideas from Agentic AI
forum discussions without treating every observation as an implementation
commitment. It provides a public-safe place to preserve useful context,
identify themes, and decide whether feedback should be parked, researched,
documented, or converted into a GitHub issue.

## How to use this log

1. Record feedback in generic, public-safe language.
2. Separate what a participant asked or observed from a possible project
   response.
3. Link feedback to relevant taxonomy buckets when that helps organize it.
4. Assign a decision status without implying that a feature is committed.
5. Convert accepted work into a scoped issue before implementation.
6. Update the entry with an issue or pull request link when one exists.

Use this reusable template:

```md
### YYYY-MM-DD - Short feedback title

- **Context/event:** Agentic AI forum
- **Source type:** forum participant / demo observer / self-observation / follow-up discussion
- **Feedback or question:**
- **Related taxonomy bucket(s):**
- **Public/private safety concern:**
- **Possible action:**
- **Decision status:** new / parked / accepted / rejected / needs research / converted to issue
- **Linked issue/PR:**
- **Notes:**
```

## Public-safety rules

- Do not record private attendee names unless the person and attribution are
  already public or explicitly approved.
- Do not include employer-specific details or imply employer endorsement.
- Do not include internal workflows or internal URLs.
- Do not include screenshots from work systems.
- Do not include private prompts, logs, traces, memory or state snapshots,
  credentials, secrets, regulated data, or proprietary examples.
- Do not include generated catalogs or scan findings from private
  collections.
- Convert feedback into generic, synthetic, public-safe language before
  publishing it.
- When ownership, consent, or publication rights are unclear, keep the
  original detail out of this repository.

## Feedback entries

### 2026-06-16 - Clarify whether this is an agent

- **Context/event:** Agentic AI forum
- **Source type:** anticipated forum question
- **Feedback or question:** Is `agent-librarian` an agent if it does not use an
  LLM?
- **Related taxonomy bucket(s):** Identity, Tools, Planning and orchestration,
  Guardrails and governance
- **Public/private safety concern:** Avoid overclaiming autonomy.
- **Possible action:** Improve docs to distinguish the deterministic CLI
  backend from the planned LLM interaction layer.
- **Decision status:** accepted
- **Linked issue/PR:** #45, #46, #47, #48
- **Notes:** Use "agentic infrastructure component" or "artifact-librarian
  backend" when precision matters.

### 2026-06-16 - Explain which layer is authoritative

- **Context/event:** Agentic AI forum
- **Source type:** anticipated demo observer question
- **Feedback or question:** If an LLM summarizes a catalog run, which output
  should a reviewer trust?
- **Related taxonomy bucket(s):** Tools, Outputs and schemas, Evaluation and
  observability, Guardrails and governance
- **Public/private safety concern:** Avoid presenting model-generated
  summaries as deterministic findings.
- **Possible action:** State that CLI-generated files remain the source of
  truth and that LLM summaries are review aids.
- **Decision status:** accepted
- **Linked issue/PR:** #47, #48, #55
- **Notes:** Preserve direct links from summaries to generated review
  artifacts.

### 2026-06-16 - Make approval boundaries visible

- **Context/event:** Agentic AI forum
- **Source type:** anticipated follow-up discussion
- **Feedback or question:** Which actions can the future LLM layer take
  directly, and which actions require user approval?
- **Related taxonomy bucket(s):** Planning and orchestration, Guardrails and
  governance, State
- **Public/private safety concern:** Do not imply autonomous approval,
  publication, or arbitrary command execution.
- **Possible action:** Define proposed-command, refusal, approval, and
  run-state artifacts before implementing a runtime wrapper.
- **Decision status:** converted to issue
- **Linked issue/PR:** #48, #49, #54
- **Notes:** Keep approval events explicit and inspectable.

## Parking lot

Use this section for ideas that are relevant but not ready for an issue.
Parking an item is not acceptance or rejection.

- Provider selection criteria for an optional LLM layer.
- Additional public-safe forum demo examples.
- A future method for comparing deterministic catalogs across runs.

## Decision status legend

| Status | Meaning |
| --- | --- |
| `new` | Captured but not yet reviewed. |
| `parked` | Worth retaining, but not currently prioritized or scoped. |
| `accepted` | Direction is accepted; implementation still requires appropriate scope. |
| `rejected` | Considered and intentionally not planned, with rationale recorded in notes. |
| `needs research` | More evidence, design work, or safety review is required. |
| `converted to issue` | Follow-up work is tracked in a GitHub issue. |

## Related docs

- [v0.4 roadmap](roadmap-v0.4.md)
- [Forum demo runbook](forum-demo-runbook.md)
- [Showcase brief](showcase-brief.md)
- [Taxonomy-aligned architecture map](taxonomy-architecture-map.md)
- [Public-safe adoption guide](adoption-guide.md)
- [Public safety](public-safety.md)
