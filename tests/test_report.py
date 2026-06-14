from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_librarian.cli import main


def _write_generated_catalog(catalog_dir: Path) -> None:
    catalog_dir.mkdir()
    documents = {
        "index.json": {
            "schema_version": "0.1.0",
            "source_root": "synthetic-collection",
            "synthetic_example": True,
            "entry_count": 2,
            "entries": [
                {
                    "discoverability_warnings": [
                        "weak_description",
                        "missing_outputs",
                    ]
                },
                {
                    "discoverability_warnings": [
                        "duplicate_candidate",
                        "future_warning_code",
                    ]
                },
            ],
        },
        "diagnostics.json": {
            "schema_version": "0.1.0",
            "source_root": "synthetic-collection",
            "generated_at": "2026-06-14T12:00:00Z",
            "summary": {
                "total_files_seen": 4,
                "parsed": 1,
                "partial": 1,
                "skipped": 1,
                "failed": 1,
            },
            "files": [
                {
                    "status": "partial",
                    "warnings": [
                        "weak_description",
                        "unsupported_file_type",
                    ],
                }
            ],
        },
        "overlap-report.json": {
            "schema_version": "0.1.0",
            "source_root": "synthetic-collection",
            "synthetic_example": True,
            "candidate_count": 1,
            "candidates": [
                {
                    "overlap_type": "duplicate",
                }
            ],
        },
    }
    for file_name, document in documents.items():
        (catalog_dir / file_name).write_text(
            json.dumps(document, indent=2) + "\n",
            encoding="utf-8",
        )


def test_report_summarizes_generated_catalog(
    tmp_path: Path,
    capsys,
) -> None:
    catalog_dir = tmp_path / "generated-catalog"
    _write_generated_catalog(catalog_dir)

    exit_code = main(["report", str(catalog_dir)])

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "agent-librarian review report" in captured.out
    assert "- Catalog entries: 2" in captured.out
    assert "- Parsed files: 1" in captured.out
    assert "- Partial files: 1" in captured.out
    assert "- Failed files: 1" in captured.out
    assert "- Catalog warnings: 2" in captured.out
    assert "- weak_description: 1" in captured.out
    assert "- missing_outputs: 1" in captured.out
    assert "- unsupported_file_type: 1" in captured.out
    assert "- duplicate_candidate: 1" in captured.out
    assert "- overlap_candidate: 0" in captured.out
    assert "future_warning_code: 1 (unknown; review needed)" in captured.out
    assert "Suggested human review" in captured.out
    assert (
        "Warnings and overlap candidates are review prompts, not decisions."
        in captured.out
    )
    assert captured.err == ""


@pytest.mark.parametrize(
    "missing_file",
    ["index.json", "diagnostics.json", "overlap-report.json"],
)
def test_report_fails_clearly_when_required_file_is_missing(
    tmp_path: Path,
    capsys,
    missing_file: str,
) -> None:
    catalog_dir = tmp_path / "generated-catalog"
    _write_generated_catalog(catalog_dir)
    (catalog_dir / missing_file).unlink()

    exit_code = main(["report", str(catalog_dir)])

    assert exit_code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert (
        f"Report error: required generated file is missing: {missing_file}"
        in captured.err
    )


def test_report_does_not_modify_generated_files(tmp_path: Path) -> None:
    catalog_dir = tmp_path / "generated-catalog"
    _write_generated_catalog(catalog_dir)
    before = {
        path.name: path.read_bytes()
        for path in catalog_dir.iterdir()
        if path.is_file()
    }

    exit_code = main(["report", str(catalog_dir)])

    after = {
        path.name: path.read_bytes()
        for path in catalog_dir.iterdir()
        if path.is_file()
    }
    assert exit_code == 0
    assert after == before
