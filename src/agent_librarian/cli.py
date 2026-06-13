from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .overlap import find_overlaps
from .parsers import parse_artifact
from .renderers import build_index, build_overlap_report, write_outputs
from .scanner import scan_files
from .warnings import apply_warnings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-librarian",
        description="Catalog local agentic AI artifacts without executing them.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    catalog = subparsers.add_parser(
        "catalog", help="Scan a directory and generate catalog outputs."
    )
    catalog.add_argument("input_dir", type=Path, help="Directory to scan.")
    catalog.add_argument(
        "--out", required=True, type=Path, help="Directory for generated outputs."
    )
    return parser


def run_catalog(input_dir: Path, output_dir: Path) -> list[Path]:
    root = input_dir.resolve()
    out = output_dir.resolve()
    entries = []
    for path in scan_files(root, out):
        entry = parse_artifact(path, root)
        source_text = path.read_text(encoding="utf-8")
        apply_warnings(entry, source_text)
        entries.append(entry)

    candidates = find_overlaps(entries)
    index = build_index(root, entries)
    overlap_report = build_overlap_report(root, candidates)
    return write_outputs(out, index, overlap_report)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "catalog":
        try:
            paths = run_catalog(args.input_dir, args.out)
        except (OSError, ValueError, UnicodeError) as exc:
            parser.error(str(exc))
        print(f"Cataloged artifacts into {paths[0].parent}")
        for path in paths:
            print(f"- {path.name}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
