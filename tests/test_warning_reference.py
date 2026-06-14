from __future__ import annotations

import re
from pathlib import Path

from agent_librarian.warning_codes import ACTIVE_WARNING_CODES


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WARNING_REFERENCE = REPOSITORY_ROOT / "docs" / "warnings-and-overlap.md"
WARNING_TABLE_ROW = re.compile(r"^\| `([a-z][a-z0-9_]*)` \|", re.MULTILINE)


def test_all_active_warning_codes_are_documented() -> None:
    documented_codes = set(
        WARNING_TABLE_ROW.findall(WARNING_REFERENCE.read_text(encoding="utf-8"))
    )

    undocumented_codes = ACTIVE_WARNING_CODES - documented_codes

    assert not undocumented_codes, (
        "Active warning codes missing from docs/warnings-and-overlap.md: "
        f"{sorted(undocumented_codes)}"
    )
