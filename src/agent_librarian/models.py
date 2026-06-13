from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


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


ParseStatus = Literal["parsed", "partial", "skipped", "failed"]


@dataclass
class FileDiagnostic:
    source_path: str
    status: ParseStatus
    parser: str | None
    artifact_type_guess: str | None = None
    taxonomy_bucket_guess: str | None = None
    warnings: list[str] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DiagnosticsSummary:
    total_files_seen: int = 0
    parsed: int = 0
    partial: int = 0
    skipped: int = 0
    failed: int = 0

    @classmethod
    def from_files(cls, files: list[FileDiagnostic]) -> DiagnosticsSummary:
        counts = {status: 0 for status in ("parsed", "partial", "skipped", "failed")}
        for diagnostic in files:
            counts[diagnostic.status] += 1
        return cls(total_files_seen=len(files), **counts)

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass
class DiagnosticsReport:
    schema_version: str
    source_root: str
    generated_at: str
    summary: DiagnosticsSummary
    files: list[FileDiagnostic]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source_root": self.source_root,
            "generated_at": self.generated_at,
            "summary": self.summary.to_dict(),
            "files": [diagnostic.to_dict() for diagnostic in self.files],
        }


@dataclass
class ParseResult:
    entry: CatalogEntry | None
    diagnostic: FileDiagnostic
    source_text: str | None = field(default=None, repr=False)
