import hashlib
import json
from pathlib import Path

from jsonschema import FormatChecker
from jsonschema.validators import validator_for


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    REPO_ROOT
    / "src"
    / "agent_librarian"
    / "schema_data"
    / "source-manifest.schema.json"
)
EXAMPLE_ROOT = REPO_ROOT / "examples" / "source-snapshots" / "synthetic-team-space"
EXAMPLE_PATH = EXAMPLE_ROOT / "source-manifest.json"


def _load_schema_and_example() -> tuple[dict, dict]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    example = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    return schema, example


def test_source_manifest_schema_validates_synthetic_snapshot_example() -> None:
    schema, example = _load_schema_and_example()

    validator_class = validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema, format_checker=FormatChecker())

    assert list(validator.iter_errors(example)) == []


def test_synthetic_source_manifest_uses_public_safe_placeholder_values() -> None:
    raw = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(EXAMPLE_ROOT.rglob("*"))
        if path.is_file()
    ).lower()

    assert "sharepoint.com" not in raw
    assert "http://" not in raw
    assert "https://" not in raw
    assert "private_contents_marker" not in raw
    assert "patient" not in raw
    assert "employer" not in raw


def test_source_manifest_requires_sensitivity_inheritance_and_review() -> None:
    schema, example = _load_schema_and_example()
    validator_class = validator_for(schema)
    validator = validator_class(schema, format_checker=FormatChecker())

    example["sensitivity"]["generated_outputs_inherit_sensitivity"] = False
    example["review"]["review_required"] = False
    example["export"]["source_access_read_only"] = False
    errors = list(validator.iter_errors(example))

    error_paths = {tuple(error.absolute_path) for error in errors}
    assert error_paths == {
        ("export", "source_access_read_only"),
        ("review", "review_required"),
        ("sensitivity", "generated_outputs_inherit_sensitivity"),
    }


def test_synthetic_manifest_file_metadata_matches_snapshot() -> None:
    _, example = _load_schema_and_example()
    files_root = EXAMPLE_ROOT / "files"

    recorded_paths = {
        entry["snapshot_path"] for entry in example["exported_files"]
    }
    actual_paths = {
        path.relative_to(files_root).as_posix()
        for path in files_root.rglob("*")
        if path.is_file()
    }
    assert recorded_paths == actual_paths

    for entry in example["exported_files"]:
        content = (files_root / entry["snapshot_path"]).read_bytes()
        # Older Windows worktrees may predate the fixture's eol=lf attribute.
        content = content.replace(b"\r\n", b"\n")
        assert entry["size_bytes"] == len(content)
        assert entry["sha256"] == hashlib.sha256(content).hexdigest()
