from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

import pytest

from agent_librarian.cli import main
from agent_librarian.narration import (
    GROUNDING_INSTRUCTION,
    MAX_NARRATION_TOKENS,
    AnthropicNarrationClient,
    NarrationError,
    NarrationResponse,
    serialize_narration_input,
)
from agent_librarian.presenter import present_catalog_with_narration


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GENERATED_CATALOG = REPOSITORY_ROOT / "examples" / "generated-catalog"
INPUT_FILES = ["index.json", "diagnostics.json", "overlap-report.json"]


def _copy_generated_catalog(tmp_path: Path) -> Path:
    catalog_dir = tmp_path / "generated-catalog"
    shutil.copytree(GENERATED_CATALOG, catalog_dir)
    return catalog_dir


class StubNarrationClient:
    def __init__(self, text: str = "Six artifacts require human review.") -> None:
        self.text = text
        self.calls: list[dict[str, object]] = []

    def narrate(self, **kwargs: object) -> NarrationResponse:
        self.calls.append(kwargs)
        return NarrationResponse(
            text=self.text,
            input_tokens=321,
            output_tokens=42,
        )


class FailingNarrationClient:
    def narrate(self, **kwargs: object) -> NarrationResponse:
        raise NarrationError("stubbed provider failure")


def test_default_present_is_offline_without_api_key(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    exit_code = main(
        ["present", str(catalog_dir), "--out", str(tmp_path / "out")],
        narration_client=FailingNarrationClient(),
    )

    assert exit_code == 0
    assert {path.name for path in (tmp_path / "out").iterdir()} == {
        "overview.html"
    }


def test_narrate_without_key_fails_and_writes_nothing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    output_dir = tmp_path / "out"
    stub = StubNarrationClient()
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    exit_code = main(
        [
            "present",
            str(catalog_dir),
            "--out",
            str(output_dir),
            "--narrate",
        ],
        narration_client=stub,
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "Narration requires ANTHROPIC_API_KEY" in captured.err
    assert "Re-run without --narrate" in captured.err
    assert not output_dir.exists()
    assert stub.calls == []


def test_narrated_present_writes_grounded_outputs_and_provenance(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    output_dir = tmp_path / "out"
    narrative = 'Six artifacts. <script>alert("unsafe")</script>'
    stub = StubNarrationClient(narrative)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-only-placeholder")
    before = {path.name: path.read_bytes() for path in catalog_dir.iterdir()}

    exit_code = main(
        [
            "present",
            str(catalog_dir),
            "--out",
            str(output_dir),
            "--narrate",
            "--model",
            "test-model",
        ],
        narration_client=stub,
    )

    assert exit_code == 0
    assert {path.name for path in output_dir.iterdir()} == {
        "overview.html",
        "narrative.md",
        "narrative-provenance.json",
    }
    html = (output_dir / "overview.html").read_text(encoding="utf-8")
    assert "Model-generated" in html
    assert "secondary review aid" in html
    assert "not a certification" in html
    assert narrative not in html
    assert "&lt;script&gt;alert(&quot;unsafe&quot;)&lt;/script&gt;" in html
    assert html.index("Catalog narrative") < html.index("Artifacts</h2>")
    assert "Synthetic Research Assistant" in html
    assert "Parsed 5" in html
    assert "Overlap candidates" in html

    markdown = (output_dir / "narrative.md").read_text(encoding="utf-8")
    assert markdown.startswith("# Model-generated narrative")
    assert "source of truth" in markdown
    assert narrative in markdown

    assert len(stub.calls) == 1
    call = stub.calls[0]
    assert call["model"] == "test-model"
    assert call["system_instruction"] == GROUNDING_INSTRUCTION
    assert call["max_tokens"] == MAX_NARRATION_TOKENS
    payload = call["input_payload"]
    assert isinstance(payload, str)
    decoded = json.loads(payload)
    assert [item["file"] for item in decoded] == INPUT_FILES
    expected_documents = {
        file_name: json.loads(
            (catalog_dir / file_name).read_text(encoding="utf-8")
        )
        for file_name in INPUT_FILES
    }
    assert payload == serialize_narration_input(expected_documents)

    provenance = json.loads(
        (output_dir / "narrative-provenance.json").read_text(encoding="utf-8")
    )
    assert provenance["model"] == "test-model"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", provenance["created_at"])
    assert provenance["input_files"] == INPUT_FILES
    assert provenance["input_digest"] == hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()
    assert provenance["token_usage"] == {
        "input_tokens": 321,
        "output_tokens": 42,
    }
    output = capsys.readouterr().out
    assert str(output_dir / "overview.html") in output
    assert str(output_dir / "narrative.md") in output
    assert str(output_dir / "narrative-provenance.json") in output
    assert "Token usage: 321 input, 42 output" in output
    assert "Estimated cost: not calculated; pricing is not bundled." in output
    after = {path.name: path.read_bytes() for path in catalog_dir.iterdir()}
    assert after == before


def test_narration_reads_only_allowed_generated_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    reads: list[Path] = []
    original_read_text = Path.read_text

    def recording_read_text(path: Path, *args, **kwargs) -> str:
        reads.append(path)
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", recording_read_text)
    present_catalog_with_narration(
        catalog_dir,
        tmp_path / "out",
        api_key="test-only-placeholder",
        client=StubNarrationClient(),
        created_at_factory=lambda: "2026-06-27T12:00:00Z",
    )

    assert [path.name for path in reads] == INPUT_FILES
    assert all(path.parent == catalog_dir for path in reads)


def test_narration_failure_writes_no_partial_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalog_dir = _copy_generated_catalog(tmp_path)
    output_dir = tmp_path / "out"
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-only-placeholder")

    exit_code = main(
        [
            "present",
            str(catalog_dir),
            "--out",
            str(output_dir),
            "--narrate",
        ],
        narration_client=FailingNarrationClient(),
    )

    assert exit_code == 1
    assert not output_dir.exists()


def test_missing_optional_anthropic_sdk_has_actionable_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "anthropic", None)

    with pytest.raises(NarrationError, match=r"pip install -e .*\[narrate\]"):
        AnthropicNarrationClient("test-only-placeholder")
