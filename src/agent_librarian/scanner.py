from __future__ import annotations

import os
from pathlib import Path


SUPPORTED_SUFFIXES = {".md", ".yaml", ".yml", ".json"}
IGNORED_NAMES = {
    ".git",
    ".env",
    ".venv",
    "node_modules",
    "__pycache__",
}


def scan_file_inventory(input_dir: Path, output_dir: Path | None = None) -> list[Path]:
    """Return non-ignored files without following links or reading file contents."""
    root = input_dir.resolve()
    if not root.is_dir():
        raise ValueError(f"Input directory does not exist or is not a directory: {root}")

    excluded_output = output_dir.resolve() if output_dir else None
    files: list[Path] = []

    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        kept_dirs: list[str] = []
        for dirname in dirnames:
            candidate = (current_path / dirname).resolve()
            if dirname in IGNORED_NAMES:
                continue
            if excluded_output and (
                candidate == excluded_output or excluded_output in candidate.parents
            ):
                continue
            kept_dirs.append(dirname)
        dirnames[:] = sorted(kept_dirs)

        for filename in sorted(filenames):
            path = current_path / filename
            if filename in IGNORED_NAMES or path.is_symlink():
                continue
            files.append(path)

    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def scan_files(input_dir: Path, output_dir: Path | None = None) -> list[Path]:
    """Return supported files without following links or entering ignored paths."""
    return [
        path
        for path in scan_file_inventory(input_dir, output_dir)
        if path.suffix.lower() in SUPPORTED_SUFFIXES
    ]
