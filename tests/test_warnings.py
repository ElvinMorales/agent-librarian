from agent_librarian.models import CatalogEntry
from agent_librarian.warnings import apply_warnings


def test_warnings_flag_vague_and_missing_skill_metadata() -> None:
    entry = CatalogEntry(
        id="demo",
        name="Demo",
        artifact_type="capability_module",
        taxonomy_bucket="Capability modules",
        framework_hint=None,
        source_path="SKILL.md",
        description="Helper",
        tool_scope=["all tools"],
    )

    apply_warnings(entry, "Synthetic fixture.")

    assert "weak_description" in entry.discoverability_warnings
    assert "missing_activation_trigger" in entry.discoverability_warnings
    assert "missing_inputs" in entry.discoverability_warnings
    assert "missing_outputs" in entry.discoverability_warnings
    assert "missing_output_contract" in entry.discoverability_warnings
    assert "overbroad_tool_scope" in entry.discoverability_warnings
    assert "side_effects_unclear" in entry.discoverability_warnings
    assert "missing_dependencies" in entry.discoverability_warnings
    assert "missing_examples" in entry.discoverability_warnings
    assert "missing_evals" in entry.discoverability_warnings


def test_warning_requires_review_for_possible_sensitive_text() -> None:
    entry = CatalogEntry(
        id="tool",
        name="Tool",
        artifact_type="tool_manifest",
        taxonomy_bucket="Tools",
        framework_hint=None,
        source_path="tools.yaml",
    )

    apply_warnings(entry, "password: placeholder")

    assert entry.public_safety_flags == ["possible_credential_material"]
    assert "public_safety_review_needed" in entry.discoverability_warnings
