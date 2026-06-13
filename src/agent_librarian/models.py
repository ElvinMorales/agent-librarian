from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


TAXONOMY_BUCKETS = (
    "Identity",
    "Operating style",
    "Capability modules",
    "Tools",
    "Knowledge and resources",
    "Prompts and interfaces",
    "Memory",
    "State",
    "Planning and orchestration",
    "Guardrails and governance",
    "Outputs and schemas",
    "Evaluation and observability",
    "Runtime and deployment",
    "Learning and iteration",
)


@dataclass
class CatalogEntry:
    id: str
    name: str
    artifact_type: str
    taxonomy_bucket: str
    framework_hint: str | None
    source_path: str
    description: str = ""
    purpose: str = ""
    activation_triggers: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    tool_scope: list[str] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    related_files: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    owner: str | None = None
    version: str | None = None
    public_safety_flags: list[str] = field(default_factory=list)
    discoverability_warnings: list[str] = field(default_factory=list)
    extraction: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class OverlapCandidate:
    entry_ids: list[str]
    overlap_type: str
    shared_terms: list[str]
    confidence: float
    needs_human_review: bool = True
    recommendation: str = (
        "Compare scope and contracts; consolidate or cross-reference only "
        "after human review."
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
