from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from agent_librarian.cli import main
from agent_librarian.presenter import present_catalog


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GENERATED_CATALOG = REPOSITORY_ROOT / "examples" / "generated-catalog"
REQUIRED_FILES = {"index.json", "diagnostics.json", "overlap-report.json"}


def _copy_generated_catalog(tmp_path: Path) -> Path:
    catalog_dir = tmp_path / "generated-catalog"
    shutil.copytree(GENERATED_CATALOG, catalog_dir)
    return catalog_dir


def test_present_writes_expected_generated_catalog_facts(
    tmp_path: Path,
    capsys,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    output_dir = tmp_path / "presentation"

    exit_code = main(["present", str(catalog_dir), "--out", str(output_dir)])

    assert exit_code == 0
    output_path = output_dir / "overview.html"
    html = output_path.read_text(encoding="utf-8")
    assert "Artifact Catalog Overview" in html
    assert "6 catalog entries" in html
    assert "Synthetic Research Assistant" in html
    assert "Summarize Documents" in html
    assert "Parsed 5 · Partial 1 · Failed 0 · Skipped 0" in html
    assert "Summarize Notes" in html
    assert "Shared terms:" in html
    assert "0.81" in html
    assert "Warnings and overlaps are review prompts, not decisions." in html
    assert str(output_path) in capsys.readouterr().out


@pytest.mark.parametrize("missing_file", sorted(REQUIRED_FILES))
def test_present_fails_clearly_when_required_file_is_missing(
    tmp_path: Path,
    capsys,
    missing_file: str,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    (catalog_dir / missing_file).unlink()

    exit_code = main(
        ["present", str(catalog_dir), "--out", str(tmp_path / "out")]
    )

    assert exit_code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert (
        f"Presentation error: required generated file is missing: {missing_file}"
        in captured.err
    )


def test_present_fails_clearly_for_malformed_json(
    tmp_path: Path,
    capsys,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    (catalog_dir / "diagnostics.json").write_text("{", encoding="utf-8")

    exit_code = main(
        ["present", str(catalog_dir), "--out", str(tmp_path / "out")]
    )

    assert exit_code == 1
    assert (
        "Presentation error: diagnostics.json contains invalid JSON "
        "at line 1, column 2"
        in capsys.readouterr().err
    )


def test_present_fails_clearly_for_malformed_document_shape(
    tmp_path: Path,
    capsys,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    index_path = catalog_dir / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["entries"] = "not a list"
    index_path.write_text(json.dumps(index), encoding="utf-8")

    exit_code = main(
        ["present", str(catalog_dir), "--out", str(tmp_path / "out")]
    )

    assert exit_code == 1
    assert (
        "Presentation error: index.json field 'entries' must be a list"
        in capsys.readouterr().err
    )


def test_present_does_not_modify_generated_catalog_inputs(tmp_path: Path) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    before = {
        path.name: path.read_bytes()
        for path in catalog_dir.iterdir()
        if path.is_file()
    }

    present_catalog(catalog_dir, tmp_path / "out")

    after = {
        path.name: path.read_bytes()
        for path in catalog_dir.iterdir()
        if path.is_file()
    }
    assert after == before


def test_present_reads_only_required_generated_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    source_collection = tmp_path / "source-collection"
    source_collection.mkdir()
    (source_collection / "must-not-read.md").write_text(
        "source collection marker",
        encoding="utf-8",
    )
    reads: list[Path] = []
    original_read_text = Path.read_text

    def recording_read_text(path: Path, *args, **kwargs) -> str:
        reads.append(path)
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", recording_read_text)

    present_catalog(catalog_dir, tmp_path / "out")

    assert {path.name for path in reads} == REQUIRED_FILES
    assert all(path.parent == catalog_dir for path in reads)


def test_present_is_deterministic_for_identical_inputs(tmp_path: Path) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)

    first = present_catalog(catalog_dir, tmp_path / "first").read_bytes()
    second = present_catalog(catalog_dir, tmp_path / "second").read_bytes()

    assert first == second
    assert b"2026-06-15T00:00:00Z" in first


def test_present_escapes_all_source_derived_text(tmp_path: Path) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    index_path = catalog_dir / "index.json"
    diagnostics_path = catalog_dir / "diagnostics.json"
    overlap_path = catalog_dir / "overlap-report.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    diagnostics = json.loads(diagnostics_path.read_text(encoding="utf-8"))
    overlap = json.loads(overlap_path.read_text(encoding="utf-8"))
    payload = '<script>alert("unsafe")</script>'
    index["source_root"] = payload
    index["entries"][0]["name"] = payload
    index["entries"][0]["description"] = payload
    index["entries"][0]["source_path"] = payload
    index["entries"][0]["discoverability_warnings"] = [payload]
    diagnostics["files"][0]["error"] = payload
    overlap["candidates"][0]["recommendation"] = payload
    index_path.write_text(json.dumps(index), encoding="utf-8")
    diagnostics_path.write_text(json.dumps(diagnostics), encoding="utf-8")
    overlap_path.write_text(json.dumps(overlap), encoding="utf-8")

    html = present_catalog(catalog_dir, tmp_path / "out").read_text(
        encoding="utf-8"
    )

    assert payload not in html
    assert "&lt;script&gt;alert(&quot;unsafe&quot;)&lt;/script&gt;" in html
