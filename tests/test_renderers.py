from pathlib import Path

from agent_librarian.models import CatalogEntry, FileDiagnostic
from agent_librarian.renderers import build_diagnostics, build_index, render_markdown


def test_markdown_renderer_includes_expected_sections(tmp_path: Path) -> None:
    source = tmp_path / "sample-collection"
    source.mkdir()
    entry = CatalogEntry(
        id="demo",
        name="Demo Skill",
        artifact_type="capability_module",
        taxonomy_bucket="Capability modules",
        framework_hint=None,
        source_path="skills/demo/SKILL.md",
        purpose="Demonstrate rendering.",
        activation_triggers=["A catalog needs a fixture."],
        inputs=["Text"],
        outputs=["Summary"],
        tool_scope=["Read-only local files"],
        side_effects=["None"],
        dependencies=["Python"],
        tags=["demo"],
        extraction={"confidence": 1.0},
    )

    markdown = render_markdown(build_index(source, [entry]))

    assert "# Artifact Catalog" in markdown
    assert "## Summary" in markdown
    assert "## Entries" in markdown
    assert "### Demo Skill" in markdown
    assert "Activation triggers" in markdown
    assert "Extraction confidence: 1.0" in markdown
    assert "synthetic, public-safe example collection" in markdown


def test_diagnostics_renderer_counts_statuses(tmp_path: Path) -> None:
    source = tmp_path / "collection"
    source.mkdir()
    files = [
        FileDiagnostic("clean.json", "parsed", "json"),
        FileDiagnostic("partial.md", "partial", "markdown"),
        FileDiagnostic("notes.txt", "skipped", None),
        FileDiagnostic("invalid.yaml", "failed", "yaml"),
    ]

    diagnostics = build_diagnostics(
        source, files, generated_at="2026-06-13T00:00:00Z"
    ).to_dict()

    assert diagnostics["generated_at"] == "2026-06-13T00:00:00Z"
    assert diagnostics["summary"] == {
        "total_files_seen": 4,
        "parsed": 1,
        "partial": 1,
        "skipped": 1,
        "failed": 1,
    }
