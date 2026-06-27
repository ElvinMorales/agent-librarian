from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .overlap import find_overlaps
from .parsers import parse_artifact_with_diagnostic
from .narration import DEFAULT_NARRATION_MODEL, NarrationClient
from .presenter import (
    PresentationError,
    present_catalog,
    present_catalog_with_narration,
)
from .report import ReportError, render_review_report
from .renderers import (
    build_diagnostics,
    build_index,
    build_overlap_report,
    write_outputs,
)
from .scanner import scan_file_inventory
from .validation import validate_catalog
from .warning_codes import PARTIAL_WARNING_CODES
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
    catalog.add_argument(
        "--include",
        action="append",
        default=[],
        metavar="GLOB",
        help=(
            "Only inventory files matching this glob; repeat for multiple patterns. "
            "Defaults to all non-excluded files."
        ),
    )
    catalog.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERNS",
        help=(
            "Add comma-separated relative path or name patterns to the safe "
            "default excludes; may be repeated."
        ),
    )
    catalog.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any selected file fails to parse.",
    )
    validate = subparsers.add_parser(
        "validate", help="Validate generated catalog JSON against bundled schemas."
    )
    validate.add_argument(
        "catalog_dir", type=Path, help="Directory containing generated catalog files."
    )
    report = subparsers.add_parser(
        "report",
        help="Summarize generated catalog outputs for human review.",
    )
    report.add_argument(
        "catalog_dir",
        type=Path,
        help="Directory containing generated catalog files.",
    )
    present = subparsers.add_parser(
        "present",
        help="Render an offline HTML overview from generated catalog outputs.",
    )
    present.add_argument(
        "catalog_dir",
        type=Path,
        help="Directory containing generated catalog files.",
    )
    present.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Directory for overview.html.",
    )
    present.add_argument(
        "--narrate",
        action="store_true",
        help="Add an optional grounded Anthropic narrative and provenance.",
    )
    present.add_argument(
        "--model",
        default=DEFAULT_NARRATION_MODEL,
        metavar="MODEL_ID",
        help=(
            "Anthropic model for --narrate "
            f"(default: {DEFAULT_NARRATION_MODEL})."
        ),
    )
    return parser


class StrictParseError(Exception):
    def __init__(self, failed_files: list[tuple[str, str | None]]) -> None:
        self.failed_files = failed_files
        super().__init__(f"{len(failed_files)} file(s) failed to parse")


def run_catalog(
    input_dir: Path,
    output_dir: Path,
    strict: bool = False,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
) -> list[Path]:
    root = input_dir.resolve()
    out = output_dir.resolve()
    entries = []
    file_diagnostics = []
    for path in scan_file_inventory(
        root,
        out,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    ):
        result = parse_artifact_with_diagnostic(path, root)
        if result.entry is not None and result.source_text is not None:
            apply_warnings(result.entry, result.source_text)
            result.diagnostic.warnings = list(
                dict.fromkeys(
                    result.diagnostic.warnings
                    + result.entry.discoverability_warnings
                )
            )
            if result.diagnostic.status == "partial" or (
                PARTIAL_WARNING_CODES & set(result.diagnostic.warnings)
            ):
                result.diagnostic.status = "partial"
            entries.append(result.entry)
        file_diagnostics.append(result.diagnostic)

    candidates = find_overlaps(entries)
    index = build_index(root, entries)
    overlap_report = build_overlap_report(root, candidates)
    diagnostics = build_diagnostics(root, file_diagnostics)
    paths = write_outputs(out, index, overlap_report, diagnostics)
    failed_files = [
        (diagnostic.source_path, diagnostic.error)
        for diagnostic in file_diagnostics
        if diagnostic.status == "failed"
    ]
    if strict and failed_files:
        raise StrictParseError(failed_files)
    return paths


def main(
    argv: list[str] | None = None,
    *,
    narration_client: NarrationClient | None = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "catalog":
        try:
            paths = run_catalog(
                args.input_dir,
                args.out,
                strict=args.strict,
                include_patterns=args.include,
                exclude_patterns=args.exclude,
            )
        except StrictParseError as exc:
            print(f"Strict mode: {exc}", file=sys.stderr)
            for source_path, error in exc.failed_files:
                print(f"- {source_path}: {error or 'parse failed'}", file=sys.stderr)
            return 2
        except (OSError, ValueError, UnicodeError) as exc:
            parser.error(str(exc))
        print(f"Cataloged artifacts into {paths[0].parent}")
        for path in paths:
            print(f"- {path.name}")
        return 0
    if args.command == "validate":
        results = validate_catalog(args.catalog_dir)
        for result in results:
            stream = sys.stdout if result.valid else sys.stderr
            status = "PASS" if result.valid else "FAIL"
            print(f"{status} {result.file_name}: {result.message}", file=stream)
        failures = [result for result in results if not result.valid]
        if failures:
            print(
                f"Validation failed: {len(failures)} of "
                f"{len(results)} file(s) failed.",
                file=sys.stderr,
            )
            return 1
        print(f"Validation passed: {len(results)} file(s) validated.")
        return 0
    if args.command == "report":
        try:
            report = render_review_report(args.catalog_dir)
        except ReportError as exc:
            print(f"Report error: {exc}", file=sys.stderr)
            return 1
        print(report, end="")
        return 0
    if args.command == "present":
        try:
            if args.narrate:
                result = present_catalog_with_narration(
                    args.catalog_dir,
                    args.out,
                    api_key=os.environ.get("ANTHROPIC_API_KEY"),
                    model=args.model,
                    client=narration_client,
                )
            else:
                output_path = present_catalog(args.catalog_dir, args.out)
        except PresentationError as exc:
            print(f"Presentation error: {exc}", file=sys.stderr)
            return 1
        if args.narrate:
            print(f"Rendered catalog overview to {result.overview_path}")
            print(f"Wrote model-generated narrative to {result.narrative_path}")
            print(f"Wrote narrative provenance to {result.provenance_path}")
            print(
                "Token usage: "
                f"{result.input_tokens} input, {result.output_tokens} output"
            )
            print("Estimated cost: not calculated; pricing is not bundled.")
        else:
            print(f"Rendered catalog overview to {output_path}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
