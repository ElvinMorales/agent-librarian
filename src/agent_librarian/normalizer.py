from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "use",
    "when",
    "with",
}


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        return "; ".join(f"{key}: {as_text(item)}" for key, item in value.items())
    if isinstance(value, Iterable):
        return "; ".join(as_text(item) for item in value if as_text(item))
    return str(value).strip()


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return _deduplicate(as_text(item) for item in value)
    if isinstance(value, dict):
        return _deduplicate(
            f"{key}: {as_text(item)}" if item not in (None, "") else str(key)
            for key, item in value.items()
        )
    text = as_text(value)
    if not text:
        return []
    lines = [
        re.sub(r"^\s*(?:[-*+]|\d+[.)])\s*", "", line).strip()
        for line in text.splitlines()
    ]
    return _deduplicate(line for line in lines if line)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "artifact"


def terms(*values: Any) -> set[str]:
    text = " ".join(as_text(value) for value in values).lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    normalized = set()
    for token in tokens:
        if token in STOP_WORDS or len(token) < 3:
            continue
        for suffix in ("ing", "ed", "es", "s"):
            if token.endswith(suffix) and len(token) > len(suffix) + 3:
                token = token[: -len(suffix)]
                break
        normalized.add(token)
    return normalized


def _deduplicate(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = value.strip()
        marker = cleaned.casefold()
        if cleaned and marker not in seen:
            seen.add(marker)
            result.append(cleaned)
    return result
