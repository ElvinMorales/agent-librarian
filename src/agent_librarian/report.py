from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .warning_codes import (
    ACTIVE_WARNING_CODES,
    CATALOG_WARNING_CODES,
    DIAGNOSTIC_WARNING_CODES,
    DUPLICATE_CANDIDATE,
    OVERLAP_CANDIDATE,
    OVERLAP_WARNING_CODES,
)


REQUIRED_REPORT_FILES = (
    "index.json",
    "diagnostics.json",
    "overlap-report.json",
)
DIAGNOSTIC_STATUSES = ("parsed", "partial", "failed", "skipped")
OVERLAP_TYPE_CODES = {
    "duplicate": DUPLICATE_CANDIDATE,
    "capability_overlap": OVERLAP_CANDIDATE,
}


class ReportError(Exception):
    pass


def render_review_report(catalog_dir: Path) -> str:
    documents = {
        file_name: _load_document(catalog_dir / file_name)
        for file_name in REQUIRED_REPORT_FILES
    }
    index = documents["index.json"]
    diagnostics = documents["diagnostics.json"]
    overlap_report = documents["overlap-report.json"]

    entries = _list_field(index, "entries", "index.json")
    diagnostic_files = _list_field(diagnostics, "files", "diagnostics.json")
    candidates = _list_field(
        overlap_report,
        "candidates",
        "overlap-report.json",
    )
    diagnostic_summary = _mapping_field(
        diagnostics,
        "summary",
        "diagnostics.json",
    )

    catalog_warning_counts = _warning_counts(
        entries,
        "discoverability_warnings",
        CATALOG_WARNING_CODES,
    )
    diagnostic_warning_counts = _warning_counts(
        diagnostic_files,
        "warnings",
        DIAGNOSTIC_WARNING_CODES,
    )
    overlap_warning_counts = Counter(
        code
        for candidate in candidates
        if isinstance(candidate, dict)
        for code in [OVERLAP_TYPE_CODES.get(candidate.get("overlap_type"))]
        if code is not None
    )
    unknown_warning_counts = Counter(
        code
        for code in _warning_values(entries, "discoverability_warnings")
        + _warning_values(diagnostic_files, "warnings")
        if code not in ACTIVE_WARNING_CODES
    )

    warning_lines = _warning_lines(
        catalog_warning_counts,
        diagnostic_warning_counts,
        overlap_warning_counts,
        unknown_warning_counts,
    )
    overlap_lines = [
        f"- {code}: {overlap_warning_counts.get(code, 0)}"
        for code in sorted(OVERLAP_WARNING_CODES)
    ]

    lines = [
        "agent-librarian review report",
        "",
        f"Catalog path: {catalog_dir}",
        (
            "Generated at: "
            f"{_required_scalar(diagnostics, 'generated_at', 'diagnostics.json')}"
        ),
        f"Schema version: {_required_scalar(index, 'schema_version', 'index.json')}",
        "",
        "Summary",
        f"- Catalog entries: {_required_count(index, 'entry_count', 'index.json')}",
        f"- Parsed files: {_status_count(diagnostic_summary, 'parsed')}",
        f"- Partial files: {_status_count(diagnostic_summary, 'partial')}",
        f"- Failed files: {_status_count(diagnostic_summary, 'failed')}",
        f"- Catalog warnings: {sum(catalog_warning_counts.values())}",
        (
            "- Overlap candidates: "
            f"{_required_count(overlap_report, 'candidate_count', 'overlap-report.json')}"
        ),
        "",
        "Warnings by code",
        *warning_lines,
        "",
        "Diagnostics by status",
        *[
            f"- {status}: {_status_count(diagnostic_summary, status)}"
            for status in DIAGNOSTIC_STATUSES
        ],
        "",
        "Overlap candidates",
        *overlap_lines,
        "",
        "Suggested human review",
        "- Review partial and failed files in diagnostics.json.",
        "- Review entries with warning codes in catalog.md or index.json.",
        (
            "- Review overlap candidates in overlap-report.json before "
            "consolidating anything."
        ),
        (
            "- Do not publish generated catalogs from private collections "
            "without source and output review."
        ),
        "",
        "Warnings and overlap candidates are review prompts, not decisions.",
    ]
    return "\n".join(lines) + "\n"


def _load_document(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ReportError(f"required generated file is missing: {path.name}")
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReportError(
            f"{path.name} contains invalid JSON at line {exc.lineno}, "
            f"column {exc.colno}"
        ) from exc
    except (OSError, UnicodeError) as exc:
        raise ReportError(f"could not read {path.name}: {exc}") from exc
    if not isinstance(document, dict):
        raise ReportError(f"{path.name} must contain a JSON object")
    return document


def _list_field(
    document: dict[str, Any],
    field_name: str,
    file_name: str,
) -> list[Any]:
    value = document.get(field_name)
    if not isinstance(value, list):
        raise ReportError(f"{file_name} field '{field_name}' must be a list")
    return value


def _mapping_field(
    document: dict[str, Any],
    field_name: str,
    file_name: str,
) -> dict[str, Any]:
    value = document.get(field_name)
    if not isinstance(value, dict):
        raise ReportError(f"{file_name} field '{field_name}' must be an object")
    return value


def _required_scalar(
    document: dict[str, Any],
    field_name: str,
    file_name: str,
) -> str:
    value = document.get(field_name)
    if not isinstance(value, str) or not value:
        raise ReportError(
            f"{file_name} field '{field_name}' must be a non-empty string"
        )
    return value


def _required_count(
    document: dict[str, Any],
    field_name: str,
    file_name: str,
) -> int:
    value = document.get(field_name)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ReportError(
            f"{file_name} field '{field_name}' must be a non-negative integer"
        )
    return value


def _status_count(summary: dict[str, Any], status: str) -> int:
    return _required_count(summary, status, "diagnostics.json summary")


def _warning_counts(
    items: Iterable[Any],
    field_name: str,
    allowed_codes: frozenset[str],
) -> Counter[str]:
    return Counter(
        code
        for code in _warning_values(items, field_name)
        if code in allowed_codes
    )


def _warning_values(items: Iterable[Any], field_name: str) -> list[str]:
    values = []
    for item in items:
        if not isinstance(item, dict):
            continue
        warnings = item.get(field_name, [])
        if not isinstance(warnings, list):
            continue
        values.extend(code for code in warnings if isinstance(code, str))
    return values


def _warning_lines(
    catalog_counts: Counter[str],
    diagnostic_counts: Counter[str],
    overlap_counts: Counter[str],
    unknown_counts: Counter[str],
) -> list[str]:
    lines = []
    for codes, counts in (
        (CATALOG_WARNING_CODES, catalog_counts),
        (DIAGNOSTIC_WARNING_CODES, diagnostic_counts),
        (OVERLAP_WARNING_CODES, overlap_counts),
    ):
        lines.extend(
            f"- {code}: {counts[code]}"
            for code in sorted(codes)
            if counts[code]
        )
    lines.extend(
        f"- {code}: {count} (unknown; review needed)"
        for code, count in sorted(unknown_counts.items())
    )
    return lines or ["- None"]
