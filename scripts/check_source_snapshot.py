from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import FormatChecker
from jsonschema.validators import validator_for


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "src"
    / "agent_librarian"
    / "schema_data"
    / "source-manifest.schema.json"
)
PUBLIC_SENSITIVITIES = {"public", "public-synthetic"}
UNSAFE_PATTERNS = (
    ("SharePoint host", re.compile(r"sharepoint\.com", re.IGNORECASE)),
    ("HTTP URL", re.compile(r"http://", re.IGNORECASE)),
    ("HTTPS URL", re.compile(r"https://", re.IGNORECASE)),
    ("private content marker", re.compile(r"private_contents_marker", re.IGNORECASE)),
    ("patient marker", re.compile(r"\bpatient\b", re.IGNORECASE)),
    ("client marker", re.compile(r"\bclient\b", re.IGNORECASE)),
    ("employee marker", re.compile(r"\bemployee\b", re.IGNORECASE)),
    ("password marker", re.compile(r"\bpassword\b", re.IGNORECASE)),
    ("secret marker", re.compile(r"\bsecret\b", re.IGNORECASE)),
    ("token marker", re.compile(r"\btoken\b", re.IGNORECASE)),
    ("API key marker", re.compile(r"\bapi_key\b", re.IGNORECASE)),
    (
        "environment file marker",
        re.compile(r"(?:^|[/\\\s])\.env(?:$|[/\\\s])", re.IGNORECASE),
    ),
)


def _format_json_path(parts: Any) -> str:
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def _load_json(path: Path, label: str, errors: list[str]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        errors.append(f"could not read {label} {path}: {exc}")
    except json.JSONDecodeError as exc:
        errors.append(
            f"invalid JSON in {label} {path}: line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        )
    return None


def _validate_schema(manifest: Any, schema: Any, errors: list[str]) -> None:
    try:
        validator_class = validator_for(schema)
        validator_class.check_schema(schema)
    except Exception as exc:
        errors.append(f"invalid source manifest schema {SCHEMA_PATH}: {exc}")
        return

    validator = validator_class(schema, format_checker=FormatChecker())
    validation_errors = sorted(
        validator.iter_errors(manifest),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    for error in validation_errors:
        errors.append(
            f"schema validation failed at {_format_json_path(error.absolute_path)}: "
            f"{error.message}"
        )


def _resolve_snapshot_file(
    files_root: Path, snapshot_path: str, errors: list[str]
) -> Path | None:
    if "\\" in snapshot_path:
        errors.append(
            f"exported file path must use forward slashes: {snapshot_path!r}"
        )
        return None
    relative = PurePosixPath(snapshot_path)
    if relative.is_absolute() or not relative.parts or any(
        part in {"", ".", ".."} for part in relative.parts
    ):
        errors.append(
            f"exported file path must stay under the snapshot files folder: "
            f"{snapshot_path!r}"
        )
        return None

    candidate = files_root.joinpath(*relative.parts)
    try:
        resolved = candidate.resolve()
        resolved.relative_to(files_root.resolve())
    except (OSError, ValueError):
        errors.append(
            f"exported file path escapes the snapshot files folder: {snapshot_path!r}"
        )
        return None
    return resolved


def _check_exported_files(
    snapshot_root: Path, manifest: dict[str, Any], errors: list[str]
) -> list[Path]:
    files_root = snapshot_root / "files"
    if not files_root.is_dir():
        errors.append(f"missing snapshot files folder: {files_root}")
        return []

    listed_paths: set[str] = set()
    for entry in manifest["exported_files"]:
        snapshot_path = entry["snapshot_path"]
        if snapshot_path in listed_paths:
            errors.append(f"duplicate exported file path: {snapshot_path!r}")
            continue
        listed_paths.add(snapshot_path)

        file_path = _resolve_snapshot_file(files_root, snapshot_path, errors)
        if file_path is None:
            continue
        if not file_path.is_file():
            errors.append(f"manifest references missing exported file: {snapshot_path}")
            continue

        try:
            content = file_path.read_bytes()
        except OSError as exc:
            errors.append(f"could not read exported file {snapshot_path}: {exc}")
            continue
        if len(content) != entry["size_bytes"]:
            errors.append(
                f"size mismatch for {snapshot_path}: manifest has "
                f"{entry['size_bytes']}, file has {len(content)}"
            )
        digest = hashlib.sha256(content).hexdigest()
        if digest != entry["sha256"]:
            errors.append(
                f"SHA-256 mismatch for {snapshot_path}: manifest has "
                f"{entry['sha256']}, file has {digest}"
            )
    actual_files = sorted(path for path in files_root.rglob("*") if path.is_file())
    actual_paths = {
        path.relative_to(files_root).as_posix() for path in actual_files
    }
    for unlisted in sorted(actual_paths - listed_paths):
        errors.append(f"snapshot file is not listed in the manifest: {unlisted}")
    return actual_files


def _check_public_markers(
    manifest_path: Path, exported_files: list[Path], errors: list[str]
) -> None:
    for path in [manifest_path, *exported_files]:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"could not scan {path}: {exc}")
            continue
        searchable = f"{path.name}\n{text}"
        for label, pattern in UNSAFE_PATTERNS:
            match = pattern.search(searchable)
            if match:
                line = searchable.count("\n", 0, match.start())
                errors.append(
                    f"public-safety marker in {path} at line {max(line, 1)}: {label}"
                )


def check_source_snapshot(snapshot_root: Path) -> list[str]:
    snapshot_root = snapshot_root.resolve()
    errors: list[str] = []
    if not snapshot_root.is_dir():
        return [f"snapshot directory does not exist: {snapshot_root}"]

    manifest_path = snapshot_root / "source-manifest.json"
    if not manifest_path.is_file():
        return [f"missing source manifest: {manifest_path}"]

    schema = _load_json(SCHEMA_PATH, "schema", errors)
    manifest = _load_json(manifest_path, "manifest", errors)
    if schema is None or manifest is None:
        return errors

    _validate_schema(manifest, schema, errors)
    if errors:
        return errors

    exported_files = _check_exported_files(snapshot_root, manifest, errors)
    if manifest["sensitivity"]["level"] in PUBLIC_SENSITIVITIES:
        _check_public_markers(manifest_path, exported_files, errors)
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check a local source snapshot manifest, exported files, and "
            "public-example leak markers without network access."
        )
    )
    parser.add_argument("snapshot_dir", type=Path, help="Source snapshot directory.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = check_source_snapshot(args.snapshot_dir)
    if errors:
        print(f"Source snapshot conformance FAILED ({len(errors)} error(s)):")
        for error in errors:
            print(f"- {error}")
        print(
            "This check catches structural and obvious leakage mistakes; "
            "it does not certify publication safety."
        )
        return 1

    print(f"Source snapshot conformance passed: {args.snapshot_dir}")
    print(
        "This check does not certify the snapshot or generated outputs "
        "as safe to publish."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
