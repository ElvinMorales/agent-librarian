from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPOSITORY_ROOT / "scripts" / "check_source_snapshot.py"
EXAMPLE_ROOT = (
    REPOSITORY_ROOT / "examples" / "source-snapshots" / "synthetic-team-space"
)


def _load_checker():
    spec = importlib.util.spec_from_file_location("check_source_snapshot", CHECKER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _snapshot(tmp_path: Path) -> Path:
    destination = tmp_path / "snapshot"
    shutil.copytree(EXAMPLE_ROOT, destination)
    return destination


def _manifest(snapshot: Path) -> dict:
    return json.loads((snapshot / "source-manifest.json").read_text(encoding="utf-8"))


def _write_manifest(snapshot: Path, manifest: dict) -> None:
    (snapshot / "source-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def _update_file_metadata(snapshot: Path, manifest: dict, snapshot_path: str) -> None:
    content = (snapshot / "files" / snapshot_path).read_bytes()
    entry = next(
        item for item in manifest["exported_files"]
        if item["snapshot_path"] == snapshot_path
    )
    entry["size_bytes"] = len(content)
    entry["sha256"] = hashlib.sha256(content).hexdigest()


def test_committed_synthetic_snapshot_passes(capsys) -> None:
    checker = _load_checker()

    assert checker.main([str(EXAMPLE_ROOT)]) == 0
    assert "does not certify" in capsys.readouterr().out


def test_missing_manifest_fails(tmp_path: Path, capsys) -> None:
    checker = _load_checker()
    snapshot = tmp_path / "snapshot"
    snapshot.mkdir()

    errors = checker.check_source_snapshot(snapshot)

    assert any("missing source manifest" in error for error in errors)
    assert checker.main([str(snapshot)]) == 1
    assert "Source snapshot conformance FAILED" in capsys.readouterr().out


def test_schema_invalid_manifest_fails(tmp_path: Path) -> None:
    checker = _load_checker()
    snapshot = _snapshot(tmp_path)
    manifest = _manifest(snapshot)
    del manifest["approved_scope"]
    _write_manifest(snapshot, manifest)

    errors = checker.check_source_snapshot(snapshot)

    assert any("schema validation failed" in error for error in errors)
    assert any("approved_scope" in error for error in errors)


def test_missing_exported_file_fails(tmp_path: Path) -> None:
    checker = _load_checker()
    snapshot = _snapshot(tmp_path)
    missing_path = snapshot / "files" / "Policies" / "public-safety-notes.md"
    missing_path.unlink()

    errors = checker.check_source_snapshot(snapshot)

    assert any("references missing exported file" in error for error in errors)


def test_digest_mismatch_fails(tmp_path: Path) -> None:
    checker = _load_checker()
    snapshot = _snapshot(tmp_path)
    changed_path = snapshot / "files" / "Policies" / "public-safety-notes.md"
    changed_path.write_text("changed\n", encoding="utf-8")

    errors = checker.check_source_snapshot(snapshot)

    assert any("SHA-256 mismatch" in error for error in errors)
    assert any("size mismatch" in error for error in errors)


def test_unlisted_exported_file_fails(tmp_path: Path) -> None:
    checker = _load_checker()
    snapshot = _snapshot(tmp_path)
    (snapshot / "files" / "extra.md").write_text("synthetic\n", encoding="utf-8")

    errors = checker.check_source_snapshot(snapshot)

    assert any("not listed in the manifest" in error for error in errors)


def test_path_outside_files_folder_fails(tmp_path: Path) -> None:
    checker = _load_checker()
    snapshot = _snapshot(tmp_path)
    manifest = _manifest(snapshot)
    manifest["exported_files"][0]["snapshot_path"] = "../source-manifest.json"
    _write_manifest(snapshot, manifest)

    errors = checker.check_source_snapshot(snapshot)

    assert any("must stay under" in error for error in errors)


def test_public_snapshot_with_obvious_leak_markers_fails(tmp_path: Path) -> None:
    checker = _load_checker()
    snapshot = _snapshot(tmp_path)
    manifest = _manifest(snapshot)
    snapshot_path = manifest["exported_files"][0]["snapshot_path"]
    file_path = snapshot / "files" / snapshot_path
    file_path.write_text(
        (
            "private_contents_marker https://example.sharepoint.com "
            "patient client employee password secret token api_key .env\n"
        ),
        encoding="utf-8",
    )
    _update_file_metadata(snapshot, manifest, snapshot_path)
    _write_manifest(snapshot, manifest)

    errors = checker.check_source_snapshot(snapshot)

    assert any("SharePoint host" in error for error in errors)
    assert any("private content marker" in error for error in errors)
    assert any("patient marker" in error for error in errors)
    assert any("client marker" in error for error in errors)
    assert any("employee marker" in error for error in errors)
    assert any("password marker" in error for error in errors)
    assert any("secret marker" in error for error in errors)
    assert any("token marker" in error for error in errors)
    assert any("API key marker" in error for error in errors)
    assert any("environment file marker" in error for error in errors)


def test_private_snapshot_does_not_apply_public_example_marker_policy(
    tmp_path: Path,
) -> None:
    checker = _load_checker()
    snapshot = _snapshot(tmp_path)
    manifest = copy.deepcopy(_manifest(snapshot))
    manifest["sensitivity"]["level"] = "private-local"
    manifest["sensitivity"]["may_commit_snapshot"] = False
    manifest["sensitivity"]["may_commit_generated_outputs"] = False
    snapshot_path = manifest["exported_files"][0]["snapshot_path"]
    file_path = snapshot / "files" / snapshot_path
    file_path.write_text("patient client employee\n", encoding="utf-8")
    _update_file_metadata(snapshot, manifest, snapshot_path)
    _write_manifest(snapshot, manifest)

    assert checker.check_source_snapshot(snapshot) == []
