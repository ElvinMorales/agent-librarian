from __future__ import annotations

import re

from .models import CatalogEntry
from .warning_codes import (
    MISSING_ACTIVATION_TRIGGER,
    MISSING_DEPENDENCIES,
    MISSING_DESCRIPTION,
    MISSING_EVALS,
    MISSING_EXAMPLES,
    MISSING_INPUTS,
    MISSING_OUTPUT_CONTRACT,
    MISSING_OUTPUTS,
    OVERBROAD_TOOL_SCOPE,
    PUBLIC_SAFETY_REVIEW_NEEDED,
    SIDE_EFFECTS_UNCLEAR,
    UNKNOWN_ARTIFACT_TYPE,
    WEAK_DESCRIPTION,
)


SAFETY_PATTERNS = {
    "possible_credential_material": re.compile(
        r"\b(?:api[_-]?key|password|private[_-]?key|bearer\s+[a-z0-9])\b", re.I
    ),
    "possible_private_endpoint": re.compile(
        r"https?://(?:localhost|127\.0\.0\.1|[^/\s]*\.internal)\b", re.I
    ),
    "possible_runtime_record": re.compile(
        r"\b(?:raw trace|live memory store|runtime state snapshot|real user data)\b",
        re.I,
    ),
}

DESCRIBED_TYPES = {
    "agent_definition",
    "agent_manifest",
    "capability_module",
    "prompt_template",
    "tool_manifest",
    "protocol_manifest",
}
CONTRACT_TYPES = {
    "agent_definition",
    "agent_manifest",
    "capability_module",
    "prompt_template",
}


def apply_warnings(entry: CatalogEntry, source_text: str) -> None:
    warnings: list[str] = []

    if entry.artifact_type in DESCRIBED_TYPES and not entry.description:
        warnings.append(MISSING_DESCRIPTION)
    elif entry.description and (
        len(entry.description.split()) < 5
        or entry.description.casefold() in {"helper", "useful tool", "does tasks"}
    ):
        warnings.append(WEAK_DESCRIPTION)

    if entry.artifact_type in CONTRACT_TYPES and not entry.activation_triggers:
        warnings.append(MISSING_ACTIVATION_TRIGGER)
    if entry.artifact_type in CONTRACT_TYPES and not entry.inputs:
        warnings.append(MISSING_INPUTS)
    if entry.artifact_type in CONTRACT_TYPES and not entry.outputs:
        warnings.extend([MISSING_OUTPUTS, MISSING_OUTPUT_CONTRACT])

    tool_text = " ".join(entry.tool_scope).lower()
    if any(marker in tool_text for marker in ("all tools", "any tool", "*")):
        warnings.append(OVERBROAD_TOOL_SCOPE)

    if entry.artifact_type in {"capability_module", "tool_manifest"} and not entry.side_effects:
        warnings.append(SIDE_EFFECTS_UNCLEAR)
    if entry.artifact_type in {"agent_definition", "agent_manifest", "capability_module"} and not entry.dependencies:
        warnings.append(MISSING_DEPENDENCIES)
    if entry.artifact_type in {"capability_module", "prompt_template"} and not entry.extraction.get("examples_present"):
        warnings.append(MISSING_EXAMPLES)
    if entry.artifact_type in {"agent_definition", "agent_manifest", "capability_module"} and not any(
        "eval" in item.lower() or "test" in item.lower() for item in entry.related_files
    ):
        warnings.append(MISSING_EVALS)
    if entry.artifact_type == "unknown":
        warnings.append(UNKNOWN_ARTIFACT_TYPE)

    flags = [
        flag for flag, pattern in SAFETY_PATTERNS.items() if pattern.search(source_text)
    ]
    if flags:
        entry.public_safety_flags = flags
        warnings.append(PUBLIC_SAFETY_REVIEW_NEEDED)

    entry.discoverability_warnings = _unique(warnings)


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
