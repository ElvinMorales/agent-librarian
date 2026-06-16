from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import jsonschema
import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PACKAGE_FILES = [
    "packages/claude/README.md",
    "packages/claude/CLAUDE.md",
    "packages/claude/claude-code/.claude/skills/artifact-librarian-demo/SKILL.md",
    "packages/openai/README.md",
    "packages/openai/codex/AGENTS.md",
    "packages/openai/codex/.agents/skills/artifact-librarian/SKILL.md",
    "packages/openai/codex/codex-demo-prompt.md",
    "packages/openai/codex/codex-validation-checklist.md",
    "packages/openai/gpt/instructions.md",
    "packages/openai/gpt/knowledge-manifest.md",
    "packages/openai/gpt/conversation-starters.md",
    "packages/openai/gpt/actions-future.md",
    "packages/openai/chatgpt-project/project-instructions.md",
    "packages/openai/chatgpt-project/source-files-to-upload.md",
    "packages/openai/chatgpt-project/demo-thread-prompt.md",
    "docs/demos/claude-code-end-to-end.md",
    "docs/demos/codex-end-to-end.md",
    "docs/demos/gpt-chat-end-to-end.md",
    "docs/demos/cross-platform-agent-demo.md",
    "packages/shared/conformance/checklist.md",
]

COMMAND_CAPABLE_FILES = [
    "packages/claude/CLAUDE.md",
    "packages/claude/claude-code/.claude/skills/artifact-librarian-demo/SKILL.md",
    "packages/openai/codex/AGENTS.md",
    "packages/openai/codex/.agents/skills/artifact-librarian/SKILL.md",
    "docs/demos/claude-code-end-to-end.md",
    "docs/demos/codex-end-to-end.md",
]

ADVISORY_FILES = [
    "packages/openai/gpt/instructions.md",
    "packages/openai/gpt/knowledge-manifest.md",
    "packages/openai/gpt/actions-future.md",
    "packages/openai/chatgpt-project/project-instructions.md",
    "packages/openai/chatgpt-project/source-files-to-upload.md",
    "docs/demos/gpt-chat-end-to-end.md",
]

PACKAGE_TEXT_FILES = [
    *REQUIRED_PACKAGE_FILES,
    "packages/README.md",
    "docs/portable-agent-packages.md",
]

ALLOWED_AGENT_LIBRARIAN_ACTIONS = {"catalog", "validate", "report"}
RUNTIME_WRAPPER_RE = re.compile(
    r"python -m agent_librarian\.runtime_wrapper\s+"
    r"(propose|run)\s+(catalog|validate|report)\b"
)
AGENT_LIBRARIAN_RE = re.compile(
    r"(?:^|[\"` ])agent-librarian\s+([A-Za-z0-9_-]+)"
)


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str


def _path(relative_path: str) -> Path:
    return REPOSITORY_ROOT / relative_path


def _read(relative_path: str) -> str:
    return _path(relative_path).read_text(encoding="utf-8")


def _contains_all(relative_path: str, phrases: Iterable[str]) -> list[str]:
    text = _read(relative_path).lower()
    return [phrase for phrase in phrases if phrase.lower() not in text]


def check_required_files() -> CheckResult:
    missing = [path for path in REQUIRED_PACKAGE_FILES if not _path(path).is_file()]
    if missing:
        return CheckResult("required files", False, "missing: " + ", ".join(missing))
    return CheckResult("required files", True, f"{len(REQUIRED_PACKAGE_FILES)} files found")


def check_manifest() -> CheckResult:
    schema_path = _path("packages/shared/package-manifest.schema.json")
    example_path = _path("packages/shared/package-manifest.example.yaml")

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    manifest = yaml.safe_load(example_path.read_text(encoding="utf-8"))
    jsonschema.validate(manifest, schema)

    referenced_paths: list[str] = []
    for artifact in manifest["canonical_sources"]["artifacts"]:
        referenced_paths.append(artifact["path"])
    for platform_file in manifest["platform_files"]:
        referenced_paths.append(platform_file["path"])
        referenced_paths.extend(platform_file["maps_from"])
    referenced_paths.extend(manifest["validation"]["conformance_docs"])
    referenced_paths.append(manifest["validation"]["manifest_schema"])

    missing = sorted({path for path in referenced_paths if not _path(path).exists()})
    if missing:
        return CheckResult("manifest", False, "missing references: " + ", ".join(missing))

    return CheckResult("manifest", True, "schema validates and referenced files exist")


def check_source_of_truth_language() -> CheckResult:
    required = ["source of truth", "deterministic", "generated outputs"]
    missing = {
        path: _contains_all(path, required)
        for path in [
            "packages/claude/CLAUDE.md",
            "packages/openai/codex/AGENTS.md",
            "packages/openai/gpt/instructions.md",
            "packages/openai/chatgpt-project/project-instructions.md",
        ]
    }
    failures = {path: phrases for path, phrases in missing.items() if phrases}
    if failures:
        return CheckResult("source-of-truth language", False, str(failures))
    return CheckResult("source-of-truth language", True, "package docs are grounded")


def check_exact_approval_language() -> CheckResult:
    required = ["exact approval", "runtime-wrapper", "propose"]
    missing = {
        path: _contains_all(path, required) for path in COMMAND_CAPABLE_FILES
    }
    failures = {path: phrases for path, phrases in missing.items() if phrases}
    if failures:
        return CheckResult("exact approval language", False, str(failures))
    return CheckResult("exact approval language", True, "command-capable docs include approval gates")


def check_advisory_limits() -> CheckResult:
    combined = "\n".join(_read(path).lower() for path in ADVISORY_FILES)
    required = ["advisory", "do not run the local cli by default", "upload", "paste"]
    missing = [phrase for phrase in required if phrase not in combined]
    if missing:
        return CheckResult("advisory limits", False, "missing: " + ", ".join(missing))

    forbidden_patterns = [
        "i ran agent-librarian",
        "this gpt runs agent-librarian",
        "this project runs agent-librarian",
        "executes local commands by default",
    ]
    violations: list[str] = []
    for path in ADVISORY_FILES:
        text = _read(path).lower()
        for pattern in forbidden_patterns:
            if pattern in text:
                violations.append(f"{path}: {pattern}")
    if violations:
        return CheckResult("advisory limits", False, "; ".join(violations))
    return CheckResult("advisory limits", True, "GPT/ChatGPT docs are advisory-only")


def check_safety_boundaries() -> CheckResult:
    required = ["private", "secrets", "credentials", "memory snapshots", "state snapshots"]
    no_cert = ["certify", "publication readiness"]
    combined = "\n".join(_read(path).lower() for path in PACKAGE_TEXT_FILES)
    missing = [phrase for phrase in [*required, *no_cert] if phrase not in combined]
    if missing:
        return CheckResult("safety boundaries", False, "missing: " + ", ".join(missing))
    return CheckResult("safety boundaries", True, "package docs include safety and non-certification boundaries")


def check_command_examples() -> CheckResult:
    violations: list[str] = []
    for relative_path in PACKAGE_TEXT_FILES:
        for line_number, line in enumerate(_read(relative_path).splitlines(), start=1):
            stripped = line.strip()
            if "runtime_wrapper" in stripped and "python -m agent_librarian.runtime_wrapper" in stripped:
                if not RUNTIME_WRAPPER_RE.search(line):
                    violations.append(f"{relative_path}:{line_number}: unsupported wrapper form")

            looks_like_command = (
                stripped.startswith("agent-librarian ")
                or "--approve-exact \"agent-librarian " in stripped
            )
            if not looks_like_command:
                continue

            for match in AGENT_LIBRARIAN_RE.finditer(stripped):
                action = match.group(1)
                if action in {"--help", "--version"}:
                    continue
                if action not in ALLOWED_AGENT_LIBRARIAN_ACTIONS:
                    violations.append(
                        f"{relative_path}:{line_number}: unsupported agent-librarian action {action!r}"
                    )

    if violations:
        return CheckResult("command examples", False, "; ".join(violations))
    return CheckResult("command examples", True, "command examples use documented forms")


def check_generated_outputs_clean() -> CheckResult:
    result = subprocess.run(
        ["git", "diff", "--quiet", "--", "examples/generated-catalog"],
        cwd=REPOSITORY_ROOT,
        check=False,
    )
    if result.returncode != 0:
        return CheckResult(
            "generated outputs",
            False,
            "examples/generated-catalog has uncommitted changes",
        )
    return CheckResult("generated outputs", True, "examples/generated-catalog unchanged")


def run_checks() -> list[CheckResult]:
    checks = [
        check_required_files,
        check_manifest,
        check_source_of_truth_language,
        check_exact_approval_language,
        check_advisory_limits,
        check_safety_boundaries,
        check_command_examples,
        check_generated_outputs_clean,
    ]
    results: list[CheckResult] = []
    for check in checks:
        try:
            results.append(check())
        except Exception as exc:  # pragma: no cover - printed for CLI users
            results.append(CheckResult(check.__name__, False, repr(exc)))
    return results


def main() -> int:
    results = run_checks()
    print("Package conformance checks")
    print("==========================")
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status} {result.name}: {result.detail}")
    failures = [result for result in results if not result.passed]
    if failures:
        print(f"\n{len(failures)} check(s) failed.")
        return 1
    print("\nAll package conformance checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
