from pathlib import Path

from agent_librarian.models import CatalogEntry
from agent_librarian.renderers import build_index, render_markdown


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
