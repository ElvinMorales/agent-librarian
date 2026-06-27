from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Protocol


DEFAULT_NARRATION_MODEL = "claude-haiku-4-5-20251001"
MAX_NARRATION_TOKENS = 500
NARRATION_INPUT_FILES = (
    "index.json",
    "diagnostics.json",
    "overlap-report.json",
)
GROUNDING_INSTRUCTION = """You are writing a short, plain-English summary of an already-generated artifact catalog for a human reviewer.

You are given three JSON documents: a catalog index, a diagnostics report, and an overlap report. Use only the information in these documents. Do not use outside knowledge and do not infer anything not present in the data.

Report the real numbers: how many artifacts, how many parsed vs partial vs failed vs skipped, which warnings appear and how often, and which overlap candidates exist. Refer to artifacts by their actual names from the data.

If something is ambiguous or missing, say so plainly rather than guessing.

Do not make recommendations beyond what the diagnostics and overlap reports already flag. Frame warnings and overlaps as items for human review, not decisions.

Do not certify safety, privacy, correctness, completeness, approval, compliance, or publication readiness.

Keep it concise and skimmable. Output prose only, with no code fences."""


class NarrationError(Exception):
    pass


@dataclass(frozen=True)
class NarrationResponse:
    text: str
    input_tokens: int
    output_tokens: int


class NarrationClient(Protocol):
    def narrate(
        self,
        *,
        model: str,
        system_instruction: str,
        input_payload: str,
        max_tokens: int,
    ) -> NarrationResponse: ...


class AnthropicNarrationClient:
    """Small adapter around the optional Anthropic SDK."""

    def __init__(self, api_key: str) -> None:
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise NarrationError(
                "Anthropic narration support is not installed. Install it with "
                "'python -m pip install -e \".[narrate]\"', then retry."
            ) from exc
        self._client = Anthropic(api_key=api_key)

    def narrate(
        self,
        *,
        model: str,
        system_instruction: str,
        input_payload: str,
        max_tokens: int,
    ) -> NarrationResponse:
        try:
            message = self._client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_instruction,
                messages=[{"role": "user", "content": input_payload}],
            )
            text = "".join(
                block.text
                for block in message.content
                if getattr(block, "type", None) == "text"
                and isinstance(getattr(block, "text", None), str)
            ).strip()
            if not text:
                raise NarrationError("Anthropic returned no narrative text.")
            return NarrationResponse(
                text=text,
                input_tokens=int(message.usage.input_tokens),
                output_tokens=int(message.usage.output_tokens),
            )
        except NarrationError:
            raise
        except Exception as exc:
            raise NarrationError(
                f"Anthropic narration request failed: {type(exc).__name__}."
            ) from exc


def serialize_narration_input(documents: dict[str, dict[str, Any]]) -> str:
    """Serialize only the three allowed generated JSON documents."""
    payload = [
        {"file": file_name, "document": documents[file_name]}
        for file_name in NARRATION_INPUT_FILES
    ]
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def narration_input_digest(input_payload: str) -> str:
    return hashlib.sha256(input_payload.encode("utf-8")).hexdigest()
