from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any


REQUIRED_PRESENTATION_FILES = (
    "index.json",
    "diagnostics.json",
    "overlap-report.json",
)
DIAGNOSTIC_STATUSES = ("parsed", "partial", "failed", "skipped")


class PresentationError(Exception):
    pass


def present_catalog(catalog_dir: Path, output_dir: Path) -> Path:
    """Render existing generated catalog JSON as a deterministic HTML page."""
    documents = {
        file_name: _load_document(catalog_dir / file_name)
        for file_name in REQUIRED_PRESENTATION_FILES
    }
    html = render_overview(
        documents["index.json"],
        documents["diagnostics.json"],
        documents["overlap-report.json"],
    )
    output_path = output_dir / "overview.html"
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PresentationError(f"could not write overview.html: {exc}") from exc
    return output_path


def render_overview(
    index: dict[str, Any],
    diagnostics: dict[str, Any],
    overlap_report: dict[str, Any],
) -> str:
    entries = _list_field(index, "entries", "index.json")
    diagnostic_files = _list_field(diagnostics, "files", "diagnostics.json")
    candidates = _list_field(
        overlap_report, "candidates", "overlap-report.json"
    )
    summary = _mapping_field(diagnostics, "summary", "diagnostics.json")
    entry_count = _count_field(index, "entry_count", "index.json")
    candidate_count = _count_field(
        overlap_report, "candidate_count", "overlap-report.json"
    )
    generated_at = _text_field(
        diagnostics, "generated_at", "diagnostics.json"
    )
    source_root = _text_field(index, "source_root", "index.json")
    schema_version = _text_field(index, "schema_version", "index.json")
    status_counts = {
        status: _count_field(summary, status, "diagnostics.json summary")
        for status in DIAGNOSTIC_STATUSES
    }

    entry_by_id = {
        item.get("id"): item
        for item in entries
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    artifact_cards = "\n".join(
        _artifact_card(entry, position)
        for position, entry in enumerate(entries, start=1)
    ) or _empty_state("No catalog entries were recorded.")
    diagnostic_rows = "\n".join(
        _diagnostic_row(item, position)
        for position, item in enumerate(diagnostic_files, start=1)
    ) or _empty_table_row(5, "No diagnostic rows were recorded.")
    overlap_rows = "\n".join(
        _overlap_row(candidate, entry_by_id, position)
        for position, candidate in enumerate(candidates, start=1)
    ) or _empty_table_row(4, "No overlap candidates were recorded.")

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Artifact Catalog Overview</title>
  <style>
    :root {{
      color-scheme: light;
      --paper: #f3f5f2;
      --surface: #ffffff;
      --ink: #182625;
      --muted: #5b6b68;
      --line: #cbd6d2;
      --accent: #087f78;
      --accent-soft: #dcefeb;
      --warn: #855d12;
      --danger: #9b3d32;
      --shadow: 0 10px 28px rgba(24, 38, 37, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.55;
    }}
    .page {{ width: min(1180px, calc(100% - 2rem)); margin: 0 auto; }}
    header {{
      padding: 4.5rem 0 2.5rem;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(135deg, #e7f1ee 0%, var(--paper) 60%);
    }}
    .eyebrow {{ color: var(--accent); font-weight: 750; letter-spacing: .12em; text-transform: uppercase; }}
    h1, h2, h3 {{ line-height: 1.15; }}
    h1 {{ max-width: 760px; margin: .45rem 0 .8rem; font-size: clamp(2.3rem, 6vw, 4.7rem); letter-spacing: -.045em; }}
    h2 {{ margin: 0 0 1rem; font-size: clamp(1.55rem, 3vw, 2.2rem); }}
    h3 {{ margin: 0; font-size: 1.15rem; }}
    .subtitle {{ max-width: 720px; margin: 0; color: var(--muted); font-size: 1.05rem; }}
    .meta {{ display: flex; flex-wrap: wrap; gap: .65rem 1.5rem; margin-top: 1.5rem; color: var(--muted); }}
    .mono, code {{ font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: .9em; }}
    main {{ padding: 2.5rem 0 4rem; }}
    section {{ margin-top: 3.5rem; scroll-margin-top: 1rem; }}
    .summary {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; margin-top: 0; }}
    .stat, .card, .table-shell {{ background: var(--surface); border: 1px solid var(--line); box-shadow: var(--shadow); }}
    .stat {{ padding: 1.25rem; border-radius: 14px; }}
    .stat strong {{ display: block; color: var(--accent); font-size: 2rem; line-height: 1; }}
    .stat span {{ display: block; margin-top: .55rem; color: var(--muted); }}
    .section-head {{ display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; }}
    .section-head p {{ margin: 0; color: var(--muted); }}
    .cards {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }}
    .card {{ padding: 1.35rem; border-radius: 14px; }}
    .card-top {{ display: flex; justify-content: space-between; gap: 1rem; align-items: flex-start; }}
    .path {{ margin: .45rem 0 1rem; color: var(--muted); overflow-wrap: anywhere; }}
    .description {{ margin: 0 0 1rem; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: .45rem; }}
    .chip {{ padding: .2rem .55rem; border-radius: 999px; background: var(--accent-soft); color: #075e59; font-size: .78rem; font-weight: 700; }}
    .chip.warning {{ background: #f6ead0; color: var(--warn); }}
    .details {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .75rem 1rem; margin-top: 1rem; }}
    .details dt {{ color: var(--muted); font-size: .76rem; font-weight: 750; letter-spacing: .06em; text-transform: uppercase; }}
    .details dd {{ margin: .15rem 0 0; overflow-wrap: anywhere; }}
    .table-shell {{ overflow-x: auto; border-radius: 14px; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 720px; }}
    th, td {{ padding: .85rem 1rem; text-align: left; vertical-align: top; border-bottom: 1px solid var(--line); }}
    th {{ background: #edf3f1; color: #334744; font-size: .78rem; letter-spacing: .05em; text-transform: uppercase; }}
    tbody tr:last-child td {{ border-bottom: 0; }}
    .status {{ font-weight: 750; }}
    .status-partial, .status-skipped {{ color: var(--warn); }}
    .status-failed {{ color: var(--danger); }}
    .candidate-name {{ font-weight: 700; }}
    .empty {{ color: var(--muted); font-style: italic; }}
    footer {{ padding: 2rem 0 3rem; border-top: 1px solid var(--line); color: var(--muted); }}
    footer p {{ margin: .25rem 0; }}
    @media (max-width: 760px) {{
      header {{ padding-top: 3rem; }}
      .summary, .cards {{ grid-template-columns: 1fr; }}
      .details {{ grid-template-columns: 1fr; }}
      .section-head {{ display: block; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="page">
      <div class="eyebrow">agent-librarian</div>
      <h1>Artifact Catalog Overview</h1>
      <p class="subtitle">A deterministic, offline review of generated catalog facts.</p>
      <div class="meta mono">
        <span>Source: {escape(source_root)}</span>
        <span>Generated: {escape(generated_at)}</span>
        <span>Schema: {escape(schema_version)}</span>
      </div>
    </div>
  </header>
  <main class="page">
    <section class="summary" aria-label="Catalog summary">
      <div class="stat"><strong>{entry_count}</strong><span>Artifacts</span></div>
      <div class="stat"><strong>{sum(status_counts.values())}</strong><span>Diagnostic outcomes</span></div>
      <div class="stat"><strong>{candidate_count}</strong><span>Overlap candidates</span></div>
    </section>

    <section aria-labelledby="artifacts-title">
      <div class="section-head">
        <h2 id="artifacts-title">Artifacts</h2>
        <p>{entry_count} catalog entries</p>
      </div>
      <div class="cards">{artifact_cards}</div>
    </section>

    <section aria-labelledby="diagnostics-title">
      <div class="section-head">
        <h2 id="diagnostics-title">Diagnostics</h2>
        <p>Parsed {status_counts['parsed']} · Partial {status_counts['partial']} · Failed {status_counts['failed']} · Skipped {status_counts['skipped']}</p>
      </div>
      <div class="table-shell">
        <table>
          <thead><tr><th scope="col">Source path</th><th scope="col">Status</th><th scope="col">Parser</th><th scope="col">Classification</th><th scope="col">Warnings / error</th></tr></thead>
          <tbody>{diagnostic_rows}</tbody>
        </table>
      </div>
    </section>

    <section aria-labelledby="overlap-title">
      <div class="section-head">
        <h2 id="overlap-title">Overlap candidates</h2>
        <p>{candidate_count} prompts for human review</p>
      </div>
      <div class="table-shell">
        <table>
          <thead><tr><th scope="col">Artifacts</th><th scope="col">Type</th><th scope="col">Confidence</th><th scope="col">Evidence and recommendation</th></tr></thead>
          <tbody>{overlap_rows}</tbody>
        </table>
      </div>
    </section>
  </main>
  <footer>
    <div class="page">
      <p>Generated by agent-librarian from existing catalog outputs.</p>
      <p>Warnings and overlaps are review prompts, not decisions.</p>
    </div>
  </footer>
</body>
</html>
"""


def _artifact_card(value: Any, position: int) -> str:
    entry = _object(value, f"index.json entries[{position - 1}]")
    name = _item_text(entry, "name", "Unnamed artifact")
    source_path = _item_text(entry, "source_path", "Path not provided")
    description = _item_text(entry, "description", "No description provided.")
    warnings = _string_list(entry.get("discoverability_warnings"))
    extraction = entry.get("extraction")
    confidence = (
        extraction.get("confidence") if isinstance(extraction, dict) else None
    )
    chips = [
        _chip(_item_text(entry, "artifact_type", "Type not provided")),
        _chip(_item_text(entry, "taxonomy_bucket", "Bucket not provided")),
    ]
    chips.extend(_chip(warning, warning=True) for warning in warnings)
    return f"""<article class="card">
  <div class="card-top"><h3>{escape(name)}</h3><span class="mono">#{position}</span></div>
  <p class="path mono">{escape(source_path)}</p>
  <p class="description">{escape(description)}</p>
  <div class="chips">{''.join(chips)}</div>
  <dl class="details">
    {_detail("Version", entry.get("version"))}
    {_detail("Framework", entry.get("framework_hint"))}
    {_detail("Owner", entry.get("owner"))}
    {_detail("Extraction confidence", confidence)}
    {_detail("Warnings", len(warnings))}
  </dl>
</article>"""


def _diagnostic_row(value: Any, position: int) -> str:
    item = _object(value, f"diagnostics.json files[{position - 1}]")
    status = _item_text(item, "status", "unknown")
    warnings = _string_list(item.get("warnings"))
    error = item.get("error")
    notes = warnings + ([str(error)] if error not in (None, "") else [])
    classification = " / ".join(
        part
        for part in (
            _optional_text(item.get("artifact_type_guess")),
            _optional_text(item.get("taxonomy_bucket_guess")),
        )
        if part
    )
    return f"""<tr>
  <td class="mono">{escape(_item_text(item, 'source_path', 'Path not provided'))}</td>
  <td><span class="status status-{escape(status)}">{escape(status)}</span></td>
  <td>{escape(_optional_text(item.get('parser')) or '—')}</td>
  <td>{escape(classification or '—')}</td>
  <td>{_joined_text(notes)}</td>
</tr>"""


def _overlap_row(
    value: Any,
    entry_by_id: dict[str, dict[str, Any]],
    position: int,
) -> str:
    candidate = _object(value, f"overlap-report.json candidates[{position - 1}]")
    entry_ids = _string_list(candidate.get("entry_ids"))
    artifacts = []
    for entry_id in entry_ids:
        entry = entry_by_id.get(entry_id, {})
        name = _item_text(entry, "name", entry_id)
        path = _optional_text(entry.get("source_path"))
        suffix = f'<br><span class="mono">{escape(path)}</span>' if path else ""
        artifacts.append(f'<span class="candidate-name">{escape(name)}</span>{suffix}')
    evidence = []
    shared_terms = _string_list(candidate.get("shared_terms"))
    if shared_terms:
        evidence.append("Shared terms: " + ", ".join(shared_terms))
    recommendation = _optional_text(candidate.get("recommendation"))
    if recommendation:
        evidence.append(recommendation)
    confidence = candidate.get("confidence")
    confidence_text = (
        str(confidence)
        if isinstance(confidence, (int, float)) and not isinstance(confidence, bool)
        else "—"
    )
    return f"""<tr>
  <td>{'<hr>'.join(artifacts) if artifacts else '<span class="empty">No artifact IDs provided.</span>'}</td>
  <td>{escape(_item_text(candidate, 'overlap_type', 'Not provided'))}</td>
  <td class="mono">{escape(confidence_text)}</td>
  <td>{_joined_text(evidence)}</td>
</tr>"""


def _load_document(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise PresentationError(f"required generated file is missing: {path.name}")
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PresentationError(
            f"{path.name} contains invalid JSON at line {exc.lineno}, "
            f"column {exc.colno}"
        ) from exc
    except (OSError, UnicodeError) as exc:
        raise PresentationError(f"could not read {path.name}: {exc}") from exc
    if not isinstance(document, dict):
        raise PresentationError(f"{path.name} must contain a JSON object")
    return document


def _list_field(document: dict[str, Any], field: str, file_name: str) -> list[Any]:
    value = document.get(field)
    if not isinstance(value, list):
        raise PresentationError(f"{file_name} field '{field}' must be a list")
    return value


def _mapping_field(
    document: dict[str, Any], field: str, file_name: str
) -> dict[str, Any]:
    value = document.get(field)
    if not isinstance(value, dict):
        raise PresentationError(f"{file_name} field '{field}' must be an object")
    return value


def _text_field(document: dict[str, Any], field: str, file_name: str) -> str:
    value = document.get(field)
    if not isinstance(value, str) or not value:
        raise PresentationError(
            f"{file_name} field '{field}' must be a non-empty string"
        )
    return value


def _count_field(document: dict[str, Any], field: str, file_name: str) -> int:
    value = document.get(field)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise PresentationError(
            f"{file_name} field '{field}' must be a non-negative integer"
        )
    return value


def _object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PresentationError(f"{context} must be an object")
    return value


def _item_text(document: dict[str, Any], field: str, fallback: str) -> str:
    value = document.get(field)
    return value if isinstance(value, str) and value else fallback


def _optional_text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _chip(value: str, *, warning: bool = False) -> str:
    class_name = "chip warning" if warning else "chip"
    return f'<span class="{class_name}">{escape(value)}</span>'


def _detail(label: str, value: Any) -> str:
    if value in (None, ""):
        text = "Not provided"
    elif isinstance(value, bool):
        text = "true" if value else "false"
    else:
        text = str(value)
    return f"<div><dt>{escape(label)}</dt><dd>{escape(text)}</dd></div>"


def _joined_text(values: list[str]) -> str:
    return "<br>".join(escape(value) for value in values) if values else "—"


def _empty_state(message: str) -> str:
    return f'<p class="empty">{escape(message)}</p>'


def _empty_table_row(columns: int, message: str) -> str:
    return f'<tr><td colspan="{columns}" class="empty">{escape(message)}</td></tr>'
