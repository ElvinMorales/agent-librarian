from agent_librarian.models import CatalogEntry
from agent_librarian.overlap import find_overlaps


def _skill(entry_id: str, name: str, noun: str) -> CatalogEntry:
    return CatalogEntry(
        id=entry_id,
        name=name,
        artifact_type="capability_module",
        taxonomy_bucket="Capability modules",
        framework_hint=None,
        source_path=f"{entry_id}/SKILL.md",
        description=f"Condense plain text {noun} into a concise structured summary.",
        purpose="Preserve decisions, action items, and open questions.",
        activation_triggers=["Several documents need one reviewable summary."],
        inputs=[f"Plain text {noun}"],
        outputs=["Markdown summary with decisions and action items"],
        tags=["summarization", "structured output"],
    )


def test_overlap_report_flags_similar_skills() -> None:
    entries = [
        _skill("notes", "Summarize Notes", "notes"),
        _skill("docs", "Summarize Documents", "documents"),
    ]

    candidates = find_overlaps(entries)

    assert len(candidates) == 1
    assert candidates[0].entry_ids == ["notes", "docs"]
    assert candidates[0].overlap_type in {"duplicate", "capability_overlap"}
    assert candidates[0].needs_human_review is True
    assert "overlap_candidate" in entries[0].discoverability_warnings or (
        "duplicate_candidate" in entries[0].discoverability_warnings
    )
