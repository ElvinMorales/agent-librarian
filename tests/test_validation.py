from __future__ import annotations

import json
import shutil
from importlib import resources
from pathlib import Path

import pytest

from agent_librarian.cli import main
from agent_librarian.validation import SCHEMA_FILES


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GENERATED_CATALOG = REPOSITORY_ROOT / "examples" / "generated-catalog"


def _copy_generated_catalog(tmp_path: Path) -> Path:
    catalog_dir = tmp_path / "generated-catalog"
    shutil.copytree(GENERATED_CATALOG, catalog_dir)
    return catalog_dir


def test_valid_generated_catalog_passes(tmp_path: Path, capsys) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)

    exit_code = main(["validate", str(catalog_dir)])

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "PASS index.json: schema valid" in captured.out
    assert "PASS overlap-report.json: schema valid" in captured.out
    assert "PASS diagnostics.json: schema valid" in captured.out
    assert captured.err == ""


def test_missing_index_fails(tmp_path: Path, capsys) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    (catalog_dir / "index.json").unlink()

    exit_code = main(["validate", str(catalog_dir)])

    assert exit_code != 0
    captured = capsys.readouterr()
    assert "FAIL index.json: file is missing" in captured.err


def test_malformed_json_fails(tmp_path: Path, capsys) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    (catalog_dir / "overlap-report.json").write_text("{", encoding="utf-8")

    exit_code = main(["validate", str(catalog_dir)])

    assert exit_code != 0
    captured = capsys.readouterr()
    assert "FAIL overlap-report.json: invalid JSON at line 1, column 2" in captured.err


def test_schema_invalid_json_fails(tmp_path: Path, capsys) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    index_path = catalog_dir / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["entry_count"] = "six"
    index_path.write_text(json.dumps(index), encoding="utf-8")

    exit_code = main(["validate", str(catalog_dir)])

    assert exit_code != 0
    captured = capsys.readouterr()
    assert "FAIL index.json: $.entry_count: 'six' is not of type 'integer'" in captured.err


def test_schema_invalid_catalog_entry_fails(tmp_path: Path, capsys) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    index_path = catalog_dir / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["entries"][0]["taxonomy_bucket"] = "Not a taxonomy bucket"
    index_path.write_text(json.dumps(index), encoding="utf-8")

    exit_code = main(["validate", str(catalog_dir)])

    assert exit_code != 0
    captured = capsys.readouterr()
    assert "FAIL index.json: $.entries[0].taxonomy_bucket" in captured.err
    assert "Not a taxonomy bucket" in captured.err


def test_diagnostics_is_included_in_validation(tmp_path: Path, capsys) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    diagnostics_path = catalog_dir / "diagnostics.json"
    diagnostics = json.loads(diagnostics_path.read_text(encoding="utf-8"))
    del diagnostics["summary"]
    diagnostics_path.write_text(json.dumps(diagnostics), encoding="utf-8")

    exit_code = main(["validate", str(catalog_dir)])

    assert exit_code != 0
    captured = capsys.readouterr()
    assert "FAIL diagnostics.json" in captured.err
    assert "'summary' is a required property" in captured.err


def test_validation_does_not_modify_files(tmp_path: Path) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    before = {
        path.name: path.read_bytes()
        for path in catalog_dir.iterdir()
        if path.is_file()
    }

    exit_code = main(["validate", str(catalog_dir)])

    after = {
        path.name: path.read_bytes()
        for path in catalog_dir.iterdir()
        if path.is_file()
    }
    assert exit_code == 0
    assert after == before


@pytest.mark.parametrize("schema_name", SCHEMA_FILES)
def test_packaged_schema_matches_public_schema(schema_name: str) -> None:
    packaged = (
        resources.files("agent_librarian")
        .joinpath("schema_data", schema_name)
        .read_text(encoding="utf-8")
    )
    public = (REPOSITORY_ROOT / "schemas" / schema_name).read_text(encoding="utf-8")

    assert json.loads(packaged) == json.loads(public)
