import json
from pathlib import Path

from jsonschema import FormatChecker
from jsonschema.validators import validator_for


def test_source_manifest_schema_validates_synthetic_snapshot_example() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    schema_path = (
        repo_root
        / "src"
        / "agent_librarian"
        / "schema_data"
        / "source-manifest.schema.json"
    )
    example_path = (
        repo_root
        / "examples"
        / "source-snapshots"
        / "synthetic-team-space"
        / "source-manifest.json"
    )

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads(example_path.read_text(encoding="utf-8"))

    validator_class = validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema, format_checker=FormatChecker())

    assert list(validator.iter_errors(example)) == []


def test_synthetic_source_manifest_uses_public_safe_placeholder_values() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    example_path = (
        repo_root
        / "examples"
        / "source-snapshots"
        / "synthetic-team-space"
        / "source-manifest.json"
    )

    raw = example_path.read_text(encoding="utf-8").lower()

    assert "sharepoint.com" not in raw
    assert "http://" not in raw
    assert "https://" not in raw
    assert "private_contents_marker" not in raw
    assert "patient" not in raw
    assert "employer" not in raw
