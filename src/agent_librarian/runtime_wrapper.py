from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .cli import main as cli_main


SUPPORTED_ACTIONS = ("catalog", "validate", "report")
SENSITIVITY_VALUES = (
    "synthetic-public",
    "private-local",
    "work-internal",
    "unclear",
)
SENSITIVITY_LABELS = {
    "synthetic-public": "safe synthetic/public example",
    "private-local": "private local collection",
    "work-internal": "work/client/customer/regulated collection",
    "unclear": "unclear sensitivity",
}
GENERATED_FILE_NAMES = (
    "index.json",
    "catalog.md",
    "diagnostics.json",
    "overlap-report.json",
)
NON_CERTIFICATION_NOTE = (
    "Validation and reports are review aids, not safety or publication "
    "certification."
)
APPROVAL_INSTRUCTION = (
    "Run again with --approve-exact set to the exact command string to execute."
)
SHELL_CONTROL_CHARACTERS = frozenset(";&|><`'\"\r\n\0")
SAFE_UNQUOTED_ARGUMENT = re.compile(r"^[A-Za-z0-9_./\\,:*?=@+-]+$")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m agent_librarian.runtime_wrapper",
        description=(
            "Prototype an approval-gated local wrapper around the deterministic "
            "agent-librarian CLI."
        ),
    )
    modes = parser.add_subparsers(dest="mode", required=True)
    _add_action_parsers(modes.add_parser("propose"), mode="propose")
    _add_action_parsers(modes.add_parser("run"), mode="run")
    return parser


def _add_action_parsers(
    mode_parser: argparse.ArgumentParser,
    *,
    mode: str,
) -> None:
    actions = mode_parser.add_subparsers(dest="action", required=True)
    for action in SUPPORTED_ACTIONS:
        parser = actions.add_parser(action)
        if action == "catalog":
            parser.add_argument("source_dir")
            parser.add_argument("--out", required=True, dest="output_dir")
            parser.add_argument("--include", action="append", default=[])
            parser.add_argument("--exclude", action="append", default=[])
            parser.add_argument("--strict", action="store_true")
        else:
            parser.add_argument("catalog_dir")
        parser.add_argument("--sensitivity", choices=SENSITIVITY_VALUES)
        if mode == "propose":
            parser.add_argument("--state-out", type=Path)
        else:
            parser.add_argument("--approve-exact")
            parser.add_argument("--records-out", type=Path)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    error = _validate_inputs(args)
    if error is not None:
        _print_error(error)
        return 2

    sensitivity = args.sensitivity or _infer_sensitivity(args)
    proposal = _build_proposal(args, sensitivity)

    if args.mode == "propose":
        print(json.dumps(proposal, indent=2))
        if args.state_out is not None:
            _write_json(args.state_out, _proposal_state(args, proposal))
        return 0

    return _run(args, proposal)


def _validate_inputs(args: argparse.Namespace) -> str | None:
    values = []
    if args.action == "catalog":
        values.extend([args.source_dir, args.output_dir])
        values.extend(args.include)
        values.extend(args.exclude)
    else:
        values.append(args.catalog_dir)

    for value in values:
        if not value:
            return "Paths and optional arguments must not be empty."
        if any(character in value for character in SHELL_CONTROL_CHARACTERS):
            return (
                "Paths and optional arguments must not contain shell control "
                "characters."
            )
        if "$(" in value:
            return "Command substitution syntax is not allowed."
    return None


def _infer_sensitivity(args: argparse.Namespace) -> str:
    selected_path = (
        args.source_dir if args.action == "catalog" else args.catalog_dir
    )
    return "synthetic-public" if _is_examples_path(selected_path) else "unclear"


def _is_examples_path(value: str) -> bool:
    try:
        resolved = Path(value).resolve()
        examples_roots = {
            (Path.cwd() / "examples").resolve(),
            (Path(__file__).resolve().parents[2] / "examples").resolve(),
        }
    except OSError:
        return False

    for examples_root in examples_roots:
        try:
            resolved.relative_to(examples_root)
        except ValueError:
            continue
        return True
    return False


def _build_proposal(
    args: argparse.Namespace,
    sensitivity: str,
) -> dict[str, Any]:
    exact_command = _build_exact_command(args)
    expected_reads = [_selected_read_path(args)]
    expected_writes = _expected_generated_files(args)
    warning = _sensitivity_warning(sensitivity)

    return {
        "requested_action": args.action,
        "exact_command": exact_command,
        "expected_reads": expected_reads,
        "expected_writes": expected_writes,
        "expected_generated_files": expected_writes,
        "approval_required": True,
        "approval_instruction": APPROVAL_INSTRUCTION,
        "sensitivity": sensitivity,
        "sensitivity_class": SENSITIVITY_LABELS[sensitivity],
        "sensitivity_warning": warning,
        "source_protection_note": (
            "Source files are treated as data and are not executed, edited, "
            "deleted, merged, or published."
        ),
        "non_certification_note": NON_CERTIFICATION_NOTE,
        "summary_handoff": {
            "optional": True,
            "schema": "agent/schemas/review-summary.schema.json",
            "source_of_truth": (
                "CLI-generated files and command outputs remain authoritative."
            ),
        },
    }


def _build_exact_command(args: argparse.Namespace) -> str:
    if args.action == "catalog":
        parts = [
            "agent-librarian",
            "catalog",
            _quote_argument(args.source_dir),
            "--out",
            _quote_argument(args.output_dir),
        ]
        for pattern in args.include:
            parts.extend(["--include", _quote_argument(pattern)])
        for patterns in args.exclude:
            parts.extend(["--exclude", _quote_argument(patterns)])
        if args.strict:
            parts.append("--strict")
        return " ".join(parts)

    return " ".join(
        [
            "agent-librarian",
            args.action,
            _quote_argument(args.catalog_dir),
        ]
    )


def _quote_argument(value: str) -> str:
    if SAFE_UNQUOTED_ARGUMENT.fullmatch(value):
        return value
    return f'"{value}"'


def _selected_read_path(args: argparse.Namespace) -> str:
    return args.source_dir if args.action == "catalog" else args.catalog_dir


def _expected_generated_files(args: argparse.Namespace) -> list[str]:
    if args.action != "catalog":
        return []
    separator = (
        "\\"
        if "\\" in args.output_dir and "/" not in args.output_dir
        else "/"
    )
    output = args.output_dir.rstrip("/\\")
    return [f"{output}{separator}{name}" for name in GENERATED_FILE_NAMES]


def _sensitivity_warning(sensitivity: str) -> str:
    if sensitivity == "synthetic-public":
        return (
            "Synthetic/public scope may proceed after exact-command approval; "
            "publication still requires human review."
        )
    if sensitivity == "private-local":
        return (
            "Generated outputs and explicit runtime records inherit the source "
            "collection's private sensitivity and must remain private by default."
        )
    if sensitivity == "work-internal":
        return (
            "Work, client, customer, or regulated material is blocked from "
            "prototype execution; use proposal mode only."
        )
    return (
        "Sensitivity is unclear. Execution is blocked until --sensitivity is "
        "set explicitly."
    )


def _proposal_state(
    args: argparse.Namespace,
    proposal: dict[str, Any],
) -> dict[str, Any]:
    state = _base_state(args, proposal)
    state.update(
        {
            "workflow_phase": "proposal",
            "approval_status": "pending",
            "execution_status": "not_started",
        }
    )
    return state


def _run(args: argparse.Namespace, proposal: dict[str, Any]) -> int:
    run_id = _new_id("run")
    approval_id = _new_id("approval")
    exact_command = proposal["exact_command"]

    if args.approve_exact is None:
        message = "--approve-exact is required for execution."
        _write_run_records(
            args,
            proposal,
            run_id=run_id,
            approval_id=approval_id,
            approval_status="rejected",
            execution_status="skipped",
            exit_status=2,
            failure_reason=message,
        )
        _print_error(message)
        return 2

    if args.approve_exact != exact_command:
        message = "Approval mismatch: --approve-exact must match exact_command."
        _write_run_records(
            args,
            proposal,
            run_id=run_id,
            approval_id=approval_id,
            approval_status="rejected",
            execution_status="skipped",
            exit_status=2,
            failure_reason=message,
        )
        _print_error(message)
        return 2

    sensitivity = proposal["sensitivity"]
    if sensitivity == "unclear":
        message = (
            "Sensitivity is unclear. Execution is blocked until --sensitivity "
            "is set to synthetic-public or private-local."
        )
        _write_run_records(
            args,
            proposal,
            run_id=run_id,
            approval_id=approval_id,
            approval_status="rejected",
            execution_status="skipped",
            exit_status=2,
            failure_reason=message,
        )
        _print_error(message)
        return 2
    if sensitivity == "work-internal":
        message = (
            "Execution blocked for work-internal sensitivity in this prototype."
        )
        _write_run_records(
            args,
            proposal,
            run_id=run_id,
            approval_id=approval_id,
            approval_status="rejected",
            execution_status="skipped",
            exit_status=2,
            failure_reason=message,
        )
        _print_error(message)
        return 2

    if sensitivity == "private-local":
        print(proposal["sensitivity_warning"], file=sys.stderr)

    try:
        exit_status = cli_main(_backend_arguments(args))
    except SystemExit as exc:
        exit_status = int(exc.code) if isinstance(exc.code, int) else 1

    execution_status = "succeeded" if exit_status == 0 else "failed"
    _write_run_records(
        args,
        proposal,
        run_id=run_id,
        approval_id=approval_id,
        approval_status="approved",
        execution_status=execution_status,
        exit_status=exit_status,
        failure_reason=None if exit_status == 0 else "Deterministic CLI failed.",
    )
    return exit_status


def _backend_arguments(args: argparse.Namespace) -> list[str]:
    if args.action == "catalog":
        backend_args = [
            "catalog",
            args.source_dir,
            "--out",
            args.output_dir,
        ]
        for pattern in args.include:
            backend_args.extend(["--include", pattern])
        for patterns in args.exclude:
            backend_args.extend(["--exclude", patterns])
        if args.strict:
            backend_args.append("--strict")
        return backend_args
    return [args.action, args.catalog_dir]


def _write_run_records(
    args: argparse.Namespace,
    proposal: dict[str, Any],
    *,
    run_id: str,
    approval_id: str,
    approval_status: str,
    execution_status: str,
    exit_status: int,
    failure_reason: str | None,
) -> None:
    if args.records_out is None:
        return

    generated_files = (
        proposal["expected_generated_files"]
        if args.action == "catalog" and execution_status == "succeeded"
        else []
    )
    state = _base_state(args, proposal, run_id=run_id)
    state.update(
        {
            "workflow_phase": "execution",
            "approval_status": approval_status,
            "execution_status": execution_status,
            "generated_output_paths": generated_files,
        }
    )
    approval = {
        "approval_id": approval_id,
        "run_id": run_id,
        "timestamp": _timestamp(),
        "approval_status": approval_status,
        "exact_command": proposal["exact_command"],
        "expected_reads": proposal["expected_reads"],
        "expected_writes": proposal["expected_writes"],
        "expected_generated_files": proposal["expected_generated_files"],
        "sensitivity_class": proposal["sensitivity_class"],
        "privacy_warning_shown": True,
        "scope_note": "Approval applies only to this exact command and scope.",
        "retention_scope": "Explicit user-selected records directory.",
    }
    execution = {
        "run_id": run_id,
        "approval_id": approval_id,
        "execution_timestamp": _timestamp(),
        "exact_command": proposal["exact_command"],
        "execution_status": execution_status,
        "exit_status": exit_status,
        "generated_files": generated_files,
        "failure_reason": failure_reason,
        "retry_required": execution_status == "failed",
        "reapproval_required": execution_status != "succeeded",
        "output_retention_note": (
            "CLI stdout and stderr were emitted to the caller and not retained "
            "in this record."
        ),
    }
    args.records_out.mkdir(parents=True, exist_ok=True)
    _write_json(args.records_out / "runtime-state.json", state)
    _write_json(args.records_out / "approval-log.json", approval)
    _write_json(args.records_out / "execution-record.json", execution)


def _base_state(
    args: argparse.Namespace,
    proposal: dict[str, Any],
    *,
    run_id: str | None = None,
) -> dict[str, Any]:
    state = {
        "run_id": run_id or _new_id("run"),
        "created_at": _timestamp(),
        "requested_action": args.action,
        "sensitivity_class": proposal["sensitivity_class"],
        "proposed_command": proposal["exact_command"],
        "privacy_boundary": proposal["sensitivity_warning"],
        "retention_scope": "Explicit user-selected path only.",
    }
    if args.action == "catalog":
        state.update(
            {
                "source_path": args.source_dir,
                "output_path": args.output_dir,
                "optional_arguments": _optional_arguments(args),
            }
        )
    else:
        state["catalog_dir"] = args.catalog_dir
    return state


def _optional_arguments(args: argparse.Namespace) -> list[str]:
    arguments = []
    for pattern in args.include:
        arguments.extend(["--include", pattern])
    for patterns in args.exclude:
        arguments.extend(["--exclude", patterns])
    if args.strict:
        arguments.append("--strict")
    return arguments


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def _print_error(message: str) -> None:
    print(json.dumps({"error": message}), file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
