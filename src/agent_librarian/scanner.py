from __future__ import annotations

from fnmatch import fnmatchcase
import os
from pathlib import Path
from typing import Iterable


SUPPORTED_SUFFIXES = {".md", ".yaml", ".yml", ".json"}
DEFAULT_EXCLUDE_PATTERNS = {
    ".git",
    ".env",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "examples/generated-catalog",
}
IGNORED_NAMES = DEFAULT_EXCLUDE_PATTERNS


def scan_file_inventory(
    input_dir: Path,
    output_dir: Path | None = None,
    include_patterns: Iterable[str] | None = None,
    exclude_patterns: Iterable[str] | None = None,
) -> list[Path]:
    """Return non-ignored files without following links or reading file contents."""
    root = input_dir.resolve()
    if not root.is_dir():
        raise ValueError(f"Input directory does not exist or is not a directory: {root}")

    resolved_output = output_dir.resolve() if output_dir else None
    excluded_output = (
        resolved_output
        if resolved_output is not None and resolved_output.is_relative_to(root)
        else None
    )
    includes = _clean_patterns(include_patterns)
    excludes = DEFAULT_EXCLUDE_PATTERNS | set(
        _clean_patterns(exclude_patterns, split_commas=True)
    )
    if excluded_output == root:
        return []

    files: list[Path] = []

    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        kept_dirs: list[str] = []
        for dirname in dirnames:
            candidate_path = current_path / dirname
            if candidate_path.is_symlink():
                continue
            candidate = candidate_path.resolve()
            relative = candidate.relative_to(root)
            if _matches_any(relative, excludes):
                continue
            if excluded_output and (
                candidate == excluded_output or excluded_output in candidate.parents
            ):
                continue
            kept_dirs.append(dirname)
        dirnames[:] = sorted(kept_dirs)

        for filename in sorted(filenames):
            path = current_path / filename
            relative = path.relative_to(root)
            if path.is_symlink() or _matches_any(relative, excludes):
                continue
            if includes and not _matches_any(relative, includes):
                continue
            files.append(path)

    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def scan_files(
    input_dir: Path,
    output_dir: Path | None = None,
    include_patterns: Iterable[str] | None = None,
    exclude_patterns: Iterable[str] | None = None,
) -> list[Path]:
    """Return supported files without following links or entering ignored paths."""
    return [
        path
        for path in scan_file_inventory(
            input_dir,
            output_dir,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        )
        if path.suffix.lower() in SUPPORTED_SUFFIXES
    ]


def _clean_patterns(
    patterns: Iterable[str] | None, *, split_commas: bool = False
) -> tuple[str, ...]:
    cleaned: list[str] = []
    for value in patterns or ():
        candidates = value.split(",") if split_commas else [value]
        cleaned.extend(
            candidate.strip().replace("\\", "/")
            for candidate in candidates
            if candidate.strip()
        )
    return tuple(cleaned)


def _matches_any(relative: Path, patterns: Iterable[str]) -> bool:
    path = relative.as_posix()
    for pattern in patterns:
        if "/" not in pattern:
            if any(fnmatchcase(part, pattern) for part in relative.parts):
                return True
            continue
        if fnmatchcase(path, pattern):
            return True
        if pattern.startswith("**/") and fnmatchcase(path, pattern[3:]):
            return True
    return False
