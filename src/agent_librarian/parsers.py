from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from .models import CatalogEntry, FileDiagnostic, ParseResult
from .normalizer import as_list, as_text, slugify
from .scanner import SUPPORTED_SUFFIXES


SECTION_ALIASES = {
    "description": ("description",),
    "purpose": ("purpose",),
    "activation_triggers": ("when to use", "activation triggers", "triggers"),
    "inputs": ("inputs", "input"),
    "outputs": ("outputs", "output"),
    "tool_scope": ("tools", "tool scope"),
    "side_effects": ("side effects",),
    "dependencies": ("dependencies", "requirements"),
    "examples": ("examples", "example"),
}


def parse_artifact(path: Path, root: Path) -> CatalogEntry:
    entry, _, _ = _parse_artifact(path, root)
    return entry


def parse_artifact_with_diagnostic(path: Path, root: Path) -> ParseResult:
    relative_path = path.relative_to(root).as_posix()
    suffix = path.suffix.lower()
    parser = _parser_name(suffix)
    if suffix not in SUPPORTED_SUFFIXES:
        return ParseResult(
            entry=None,
            diagnostic=FileDiagnostic(
                source_path=relative_path,
                status="skipped",
                parser=None,
                warnings=["unsupported_file_type"],
            ),
        )

    artifact_type, bucket, _ = classify_artifact(path, relative_path, {})
    try:
        entry, text, parser_warnings = _parse_artifact(path, root)
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as exc:
        return ParseResult(
            entry=None,
            diagnostic=FileDiagnostic(
                source_path=relative_path,
                status="failed",
                parser=parser,
                artifact_type_guess=artifact_type,
                taxonomy_bucket_guess=bucket,
                error=_parse_error_summary(exc, parser),
            ),
        )
    except Exception as exc:  # Keep one malformed artifact from aborting a normal run.
        return ParseResult(
            entry=None,
            diagnostic=FileDiagnostic(
                source_path=relative_path,
                status="failed",
                parser=parser,
                artifact_type_guess=artifact_type,
                taxonomy_bucket_guess=bucket,
                error=f"Unexpected parser error: {type(exc).__name__}",
            ),
        )

    return ParseResult(
        entry=entry,
        source_text=text,
        diagnostic=FileDiagnostic(
            source_path=relative_path,
            status="partial" if parser_warnings else "parsed",
            parser=parser,
            artifact_type_guess=entry.artifact_type,
            taxonomy_bucket_guess=entry.taxonomy_bucket,
            warnings=parser_warnings,
        ),
    )


def _parse_artifact(
    path: Path, root: Path
) -> tuple[CatalogEntry, str, list[str]]:
    relative_path = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    parser_warnings: list[str] = []

    if suffix == ".md":
        metadata, sections, heading, parser_warnings = _parse_markdown(text)
        source_format = "markdown"
    elif suffix in {".yaml", ".yml"}:
        loaded = yaml.safe_load(text)
        metadata = loaded if isinstance(loaded, dict) else {}
        if not isinstance(loaded, dict):
            parser_warnings.append("non_mapping_document")
        sections, heading = {}, ""
        source_format = "yaml"
    elif suffix == ".json":
        loaded = json.loads(text)
        metadata = loaded if isinstance(loaded, dict) else {}
        if not isinstance(loaded, dict):
            parser_warnings.append("non_mapping_document")
        sections, heading = {}, ""
        source_format = "json"
    else:
        raise ValueError(f"Unsupported file type: {suffix or '<none>'}")

    artifact_type, bucket, framework_hint = classify_artifact(
        path, relative_path, metadata
    )
    name = _first_value(metadata, "name", "title", "id")
    if not name:
        name = heading or _filename_name(path)

    description = _field(metadata, sections, "description")
    purpose = _field(metadata, sections, "purpose")
    if not description and purpose:
        description = purpose

    entry = CatalogEntry(
        id=_entry_id(relative_path),
        name=as_text(name),
        artifact_type=artifact_type,
        taxonomy_bucket=bucket,
        framework_hint=framework_hint,
        source_path=relative_path,
        description=description,
        purpose=purpose,
        activation_triggers=_list_field(metadata, sections, "activation_triggers"),
        inputs=_list_field(metadata, sections, "inputs"),
        outputs=_list_field(metadata, sections, "outputs"),
        tool_scope=_list_field(metadata, sections, "tool_scope"),
        side_effects=_list_field(metadata, sections, "side_effects"),
        dependencies=_list_field(metadata, sections, "dependencies"),
        related_files=as_list(
            _first_value(metadata, "related_files", "related", "references")
        ),
        tags=as_list(_first_value(metadata, "tags", "keywords")),
        owner=as_text(_first_value(metadata, "owner", "maintainer")) or None,
        version=as_text(_first_value(metadata, "version")) or None,
        extraction={
            "source_format": source_format,
            "frontmatter": suffix == ".md" and bool(metadata),
            "heading_sections": sorted(sections),
            "confidence": _extraction_confidence(metadata, sections, heading),
        },
    )
    if _list_field(metadata, sections, "examples"):
        entry.extraction["examples_present"] = True
    return entry, text, parser_warnings


def classify_artifact(
    path: Path, relative_path: str, metadata: dict[str, Any]
) -> tuple[str, str, str | None]:
    name = path.name.lower()
    relative = relative_path.lower()

    if name == "skill.md":
        return "capability_module", "Capability modules", _skill_framework(relative)
    if name == "agents.md":
        return "agent_definition", "Identity", "Codex"
    if name == "claude.md":
        return "agent_definition", "Identity", "Claude"
    if name in {"agent.yaml", "agent.yml"}:
        return "agent_manifest", "Identity", _framework_from_metadata(metadata)
    if name in {"tools.yaml", "tools.yml"} or "/tools/" in f"/{relative}":
        return "tool_manifest", "Tools", _framework_from_metadata(metadata)
    if "prompt" in name or "/prompts/" in f"/{relative}":
        return "prompt_template", "Prompts and interfaces", None
    if _is_mcp_manifest(name, relative, metadata):
        return "protocol_manifest", "Runtime and deployment", "MCP"
    if name.endswith(".schema.json") or "$schema" in metadata or "/schemas/" in f"/{relative}":
        return "schema", "Outputs and schemas", None
    if "memory" in relative:
        return "memory_policy", "Memory", None
    if "state" in relative:
        return "state_strategy", "State", None
    if "governance" in relative or "guardrail" in relative or "policy" in name:
        return "governance_policy", "Guardrails and governance", None
    if "/evals/" in f"/{relative}" or "rubric" in name:
        return "evaluation", "Evaluation and observability", None
    if name == "changelog.md" or "/releases/" in f"/{relative}":
        return "iteration_record", "Learning and iteration", None
    return "unknown", "Knowledge and resources", _framework_from_metadata(metadata)


def _parse_markdown(
    text: str,
) -> tuple[dict[str, Any], dict[str, str], str, list[str]]:
    metadata: dict[str, Any] = {}
    body = text
    warnings: list[str] = []
    if text.startswith("---\n") or text.startswith("---\r\n"):
        match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", text, re.S)
        if match:
            loaded = yaml.safe_load(match.group(1))
            metadata = loaded if isinstance(loaded, dict) else {}
            if not isinstance(loaded, dict):
                warnings.append("non_mapping_frontmatter")
            body = text[match.end() :]
        else:
            warnings.append("unterminated_frontmatter")

    heading_match = re.search(r"^#\s+(.+?)\s*$", body, re.M)
    heading = heading_match.group(1).strip() if heading_match else ""
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"^#{2,6}\s+(.+?)\s*$", body, re.M))
    for index, match in enumerate(matches):
        key = match.group(1).strip().lower()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[key] = body[match.end() : end].strip()
    return metadata, sections, heading, warnings


def _parser_name(suffix: str) -> str | None:
    if suffix == ".md":
        return "markdown"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix == ".json":
        return "json"
    return None


def _parse_error_summary(exc: Exception, parser: str | None) -> str:
    if isinstance(exc, json.JSONDecodeError):
        return f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
    if isinstance(exc, yaml.YAMLError):
        mark = getattr(exc, "problem_mark", None)
        if mark is not None:
            return f"Invalid YAML at line {mark.line + 1}, column {mark.column + 1}"
        return "Invalid YAML syntax"
    if isinstance(exc, UnicodeDecodeError):
        return f"Could not decode UTF-8 at byte offset {exc.start}"
    if isinstance(exc, OSError):
        detail = exc.strerror or type(exc).__name__
        return f"Could not read file: {detail}"
    return f"Invalid {parser or 'file'} syntax"


def _field(
    metadata: dict[str, Any], sections: dict[str, str], canonical: str
) -> str:
    aliases = SECTION_ALIASES[canonical]
    value = _first_value(metadata, canonical, *aliases)
    if value not in (None, ""):
        return as_text(value)
    for alias in aliases:
        if sections.get(alias):
            return as_text(sections[alias])
    return ""


def _list_field(
    metadata: dict[str, Any], sections: dict[str, str], canonical: str
) -> list[str]:
    aliases = SECTION_ALIASES[canonical]
    value = _first_value(metadata, canonical, *aliases)
    if value not in (None, ""):
        return as_list(value)
    for alias in aliases:
        if sections.get(alias):
            return as_list(sections[alias])
    return []


def _first_value(metadata: dict[str, Any], *keys: str) -> Any:
    normalized = {str(key).lower().replace("-", "_"): value for key, value in metadata.items()}
    for key in keys:
        candidate = key.lower().replace(" ", "_").replace("-", "_")
        if candidate in normalized:
            return normalized[candidate]
    return None


def _filename_name(path: Path) -> str:
    if path.name.lower() == "skill.md":
        return path.parent.name.replace("-", " ").title()
    return path.stem.replace("-", " ").replace("_", " ").title()


def _entry_id(relative_path: str) -> str:
    stem = relative_path.rsplit(".", 1)[0]
    return slugify(stem.replace("/", "-"))


def _skill_framework(relative: str) -> str | None:
    if ".claude" in relative or "claude" in relative:
        return "Claude"
    if ".codex" in relative or "codex" in relative:
        return "Codex"
    return None


def _framework_from_metadata(metadata: dict[str, Any]) -> str | None:
    value = _first_value(metadata, "framework", "framework_hint", "protocol")
    return as_text(value) or None


def _is_mcp_manifest(name: str, relative: str, metadata: dict[str, Any]) -> bool:
    if "mcp" in name or "/mcp/" in f"/{relative}":
        return True
    keys = {str(key).lower() for key in metadata}
    return bool(keys & {"mcpservers", "mcp_servers"}) or metadata.get("protocol") == "mcp"


def _extraction_confidence(
    metadata: dict[str, Any], sections: dict[str, str], heading: str
) -> float:
    signals = int(bool(metadata)) + int(bool(sections)) + int(bool(heading))
    return round(0.4 + signals * 0.2, 2)
