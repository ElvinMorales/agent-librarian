from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from agent_librarian.cli import main


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MALFORMED_FIXTURE = REPOSITORY_ROOT / "tests" / "fixtures" / "malformed" / "invalid.json"


def _write_status_collection(root: Path) -> None:
    root.mkdir()
    (root / "clean.json").write_text(
        json.dumps(
            {
                "name": "synthetic-clean-server",
                "protocol": "mcp",
                "description": (
                    "Synthetic protocol manifest for deterministic parser coverage."
                ),
            }
        ),
        encoding="utf-8",
    )
    (root / "partial-prompt.md").write_text(
        """# Synthetic Partial Prompt

## Description
Prompt fixture with deliberately incomplete output metadata.

## Purpose
Exercise partial parse diagnostics.

## When to use
- A diagnostics test needs an incomplete artifact.

## Inputs
- Synthetic text.
""",
        encoding="utf-8",
    )
    (root / "ignored.txt").write_text(
        "Synthetic unsupported file.",
        encoding="utf-8",
    )
    (root / "invalid.json").write_text(
        MALFORMED_FIXTURE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )


def test_normal_mode_writes_all_diagnostic_statuses(tmp_path: Path) -> None:
    source = tmp_path / "synthetic-collection"
    output = tmp_path / "generated"
    _write_status_collection(source)

    exit_code = main(["catalog", str(source), "--out", str(output)])

    assert exit_code == 0
    assert sorted(path.name for path in output.iterdir()) == [
        "catalog.md",
        "diagnostics.json",
        "index.json",
        "overlap-report.json",
    ]

    diagnostics = json.loads((output / "diagnostics.json").read_text(encoding="utf-8"))
    schema = json.loads(
        (REPOSITORY_ROOT / "schemas" / "diagnostics.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(diagnostics)

    assert diagnostics["summary"] == {
        "total_files_seen": 4,
        "parsed": 1,
        "partial": 1,
        "skipped": 1,
        "failed": 1,
    }
    statuses = {
        item["source_path"]: item["status"] for item in diagnostics["files"]
    }
    assert statuses == {
        "clean.json": "parsed",
        "ignored.txt": "skipped",
        "invalid.json": "failed",
        "partial-prompt.md": "partial",
    }
    failed = next(
        item for item in diagnostics["files"] if item["source_path"] == "invalid.json"
    )
    assert failed["parser"] == "json"
    assert failed["artifact_type_guess"] == "unknown"
    assert failed["error"].startswith("Invalid JSON at line")

    serialized = json.dumps(diagnostics)
    assert "private_contents_marker" not in serialized
    assert "intentionally invalid JSON" not in serialized


def test_strict_mode_writes_diagnostics_and_returns_nonzero(
    tmp_path: Path, capsys
) -> None:
    source = tmp_path / "synthetic-collection"
    output = tmp_path / "generated"
    _write_status_collection(source)

    exit_code = main(
        ["catalog", str(source), "--out", str(output), "--strict"]
    )

    assert exit_code != 0
    assert (output / "diagnostics.json").is_file()
    captured = capsys.readouterr()
    assert "Strict mode: 1 file(s) failed to parse" in captured.err
    assert "invalid.json: Invalid JSON at line" in captured.err
    assert "private_contents_marker" not in captured.err


def test_clean_sample_collection_has_no_failed_diagnostics(tmp_path: Path) -> None:
    source = REPOSITORY_ROOT / "examples" / "sample-collection"
    output = tmp_path / "generated"

    exit_code = main(
        ["catalog", str(source), "--out", str(output), "--strict"]
    )

    assert exit_code == 0
    diagnostics = json.loads((output / "diagnostics.json").read_text(encoding="utf-8"))
    assert diagnostics["summary"]["failed"] == 0


def test_cli_include_limits_diagnostics_to_matching_files(tmp_path: Path) -> None:
    source = tmp_path / "synthetic-collection"
    output = tmp_path / "generated"
    source.mkdir()
    (source / "included.md").write_text("# Included", encoding="utf-8")
    (source / "excluded.yaml").write_text("name: excluded", encoding="utf-8")
    (source / "excluded.json").write_text('{"name": "excluded"}', encoding="utf-8")

    exit_code = main(
        [
            "catalog",
            str(source),
            "--out",
            str(output),
            "--include",
            "**/*.md",
        ]
    )

    diagnostics = json.loads((output / "diagnostics.json").read_text(encoding="utf-8"))
    assert exit_code == 0
    assert diagnostics["summary"]["total_files_seen"] == 1
    assert [item["source_path"] for item in diagnostics["files"]] == ["included.md"]


def test_cli_supports_repeated_include_patterns(tmp_path: Path) -> None:
    source = tmp_path / "synthetic-collection"
    output = tmp_path / "generated"
    source.mkdir()
    (source / "included.md").write_text("# Included", encoding="utf-8")
    (source / "included.yaml").write_text("name: included", encoding="utf-8")
    (source / "excluded.json").write_text('{"name": "excluded"}', encoding="utf-8")

    exit_code = main(
        [
            "catalog",
            str(source),
            "--out",
            str(output),
            "--include",
            "**/*.md",
            "--include",
            "**/*.yaml",
        ]
    )

    diagnostics = json.loads((output / "diagnostics.json").read_text(encoding="utf-8"))
    assert exit_code == 0
    assert [item["source_path"] for item in diagnostics["files"]] == [
        "included.md",
        "included.yaml",
    ]


def test_cli_excludes_do_not_leak_private_files_into_diagnostics(
    tmp_path: Path,
) -> None:
    source = tmp_path / "synthetic-collection"
    output = source / "generated"
    private = source / "private"
    private.mkdir(parents=True)
    (source / "public.md").write_text("# Public", encoding="utf-8")
    (private / "secret.md").write_text(
        "private_contents_marker",
        encoding="utf-8",
    )
    output.mkdir()
    (output / "old-diagnostics.json").write_text(
        '{"private": "private_contents_marker"}',
        encoding="utf-8",
    )

    exit_code = main(
        [
            "catalog",
            str(source),
            "--out",
            str(output),
            "--exclude",
            "private, scratch, tmp",
        ]
    )

    serialized = (output / "diagnostics.json").read_text(encoding="utf-8")
    assert exit_code == 0
    assert "private/" not in serialized
    assert "old-diagnostics.json" not in serialized
    assert "private_contents_marker" not in serialized
