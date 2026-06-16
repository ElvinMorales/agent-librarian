from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPOSITORY_ROOT / "scripts" / "check_packages.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location("check_packages", CHECKER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_package_conformance_checks_pass() -> None:
    checker = _load_checker()

    results = checker.run_checks()

    assert all(result.passed for result in results), [
        (result.name, result.detail) for result in results if not result.passed
    ]


def test_required_openai_package_files_are_tracked_by_checker() -> None:
    checker = _load_checker()

    required = set(checker.REQUIRED_PACKAGE_FILES)

    assert "packages/openai/codex/AGENTS.md" in required
    assert "packages/openai/gpt/instructions.md" in required
    assert "packages/openai/chatgpt-project/project-instructions.md" in required
    assert "docs/demos/codex-end-to-end.md" in required
    assert "docs/demos/gpt-chat-end-to-end.md" in required
