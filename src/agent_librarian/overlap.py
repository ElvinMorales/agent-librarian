from __future__ import annotations

from itertools import combinations

from .models import CatalogEntry, OverlapCandidate
from .normalizer import terms
from .warning_codes import DUPLICATE_CANDIDATE, OVERLAP_CANDIDATE


COMPARABLE_TYPES = {
    "agent_definition",
    "agent_manifest",
    "capability_module",
    "prompt_template",
    "tool_manifest",
}


def find_overlaps(entries: list[CatalogEntry]) -> list[OverlapCandidate]:
    candidates: list[OverlapCandidate] = []

    for left, right in combinations(entries, 2):
        if left.artifact_type not in COMPARABLE_TYPES:
            continue
        if left.artifact_type != right.artifact_type:
            continue

        left_terms = _entry_terms(left)
        right_terms = _entry_terms(right)
        shared = sorted(left_terms & right_terms)
        union = left_terms | right_terms
        if not union:
            continue

        jaccard = len(shared) / len(union)
        name_terms_left = terms(left.name)
        name_terms_right = terms(right.name)
        name_union = name_terms_left | name_terms_right
        name_score = (
            len(name_terms_left & name_terms_right) / len(name_union)
            if name_union
            else 0.0
        )
        confidence = round(min(1.0, jaccard * 0.75 + name_score * 0.25), 2)

        if confidence >= 0.75:
            overlap_type = "duplicate"
        elif confidence >= 0.3 and len(shared) >= 3:
            overlap_type = "capability_overlap"
        else:
            continue

        candidate = OverlapCandidate(
            entry_ids=[left.id, right.id],
            overlap_type=overlap_type,
            shared_terms=shared,
            confidence=confidence,
        )
        candidates.append(candidate)
        warning = (
            DUPLICATE_CANDIDATE
            if overlap_type == "duplicate"
            else OVERLAP_CANDIDATE
        )
        for entry in (left, right):
            if warning not in entry.discoverability_warnings:
                entry.discoverability_warnings.append(warning)

    return sorted(candidates, key=lambda item: (-item.confidence, item.entry_ids))


def _entry_terms(entry: CatalogEntry) -> set[str]:
    return terms(
        entry.name,
        entry.description,
        entry.purpose,
        entry.tags,
        entry.activation_triggers,
        entry.inputs,
        entry.outputs,
    )
