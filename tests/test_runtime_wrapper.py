from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_librarian.runtime_wrapper import main


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_COLLECTION = REPOSITORY_ROOT / "examples" / "sample-collection"


def _proposal(argv: list[str], capsys) -> dict:
    exit_code = main(["propose", *argv])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.err == ""
    return json.loads(captured.out)


def _approved_catalog(
    output_dir: Path,
    capsys,
    *,
    records_out: Path | None = None,
) -> int:
    source = str(SAMPLE_COLLECTION)
    output = str(output_dir)
    exact_command = f"agent-librarian catalog {source} --out {output}"
    argv = [
        "run",
        "catalog",
        source,
        "--out",
        output,
        "--sensitivity",
        "synthetic-public",
        "--approve-exact",
        exact_command,
    ]
    if records_out is not None:
        argv.extend(["--records-out", str(records_out)])
    exit_code = main(argv)
    capsys.readouterr()
    return exit_code


def test_catalog_proposal_has_exact_scope_and_does_not_execute(
    tmp_path: Path,
    capsys,
) -> None:
    output = tmp_path / "generated"
    proposal = _proposal(
        [
            "catalog",
            "examples/sample-collection",
            "--out",
            str(output),
        ],
        capsys,
    )

    assert proposal["requested_action"] == "catalog"
    assert proposal["exact_command"] == (
        "agent-librarian catalog examples/sample-collection "
        f"--out {output}"
    )
    assert proposal["expected_reads"] == ["examples/sample-collection"]
    assert proposal["expected_writes"] == [
        str(output / "index.json"),
        str(output / "catalog.md"),
        str(output / "diagnostics.json"),
        str(output / "overlap-report.json"),
    ]
    assert proposal["approval_required"] is True
    assert not output.exists()


@pytest.mark.parametrize("action", ["validate", "report"])
def test_read_only_proposals_require_approval(action: str, capsys) -> None:
    proposal = _proposal(
        [action, "examples/generated-catalog"],
        capsys,
    )

    assert proposal["exact_command"] == (
        f"agent-librarian {action} examples/generated-catalog"
    )
    assert proposal["expected_reads"] == ["examples/generated-catalog"]
    assert proposal["expected_writes"] == []
    assert proposal["approval_required"] is True


def test_unsupported_action_is_rejected() -> None:
    with pytest.raises(SystemExit):
        main(["propose", "delete", "examples/sample-collection"])


def test_run_requires_exact_approval(capsys) -> None:
    exit_code = main(
        ["run", "report", "examples/generated-catalog"]
    )

    assert exit_code == 2
    assert "--approve-exact is required" in capsys.readouterr().err


def test_run_rejects_approval_mismatch(capsys) -> None:
    exit_code = main(
        [
            "run",
            "report",
            "examples/generated-catalog",
            "--approve-exact",
            "wrong command",
        ]
    )

    assert exit_code == 2
    assert "Approval mismatch" in capsys.readouterr().err


def test_approval_is_command_specific(capsys) -> None:
    exit_code = main(
        [
            "run",
            "validate",
            "examples/generated-catalog",
            "--approve-exact",
            "agent-librarian report examples/generated-catalog",
        ]
    )

    assert exit_code == 2
    assert "Approval mismatch" in capsys.readouterr().err


def test_approved_catalog_validate_and_report_execute(
    tmp_path: Path,
    capsys,
) -> None:
    catalog_dir = tmp_path / "generated"
    assert _approved_catalog(catalog_dir, capsys) == 0

    validate_command = f"agent-librarian validate {catalog_dir}"
    validate_exit = main(
        [
            "run",
            "validate",
            str(catalog_dir),
            "--sensitivity",
            "synthetic-public",
            "--approve-exact",
            validate_command,
        ]
    )
    validate_output = capsys.readouterr()

    report_command = f"agent-librarian report {catalog_dir}"
    report_exit = main(
        [
            "run",
            "report",
            str(catalog_dir),
            "--sensitivity",
            "synthetic-public",
            "--approve-exact",
            report_command,
        ]
    )
    report_output = capsys.readouterr()

    assert validate_exit == 0
    assert "Validation passed" in validate_output.out
    assert report_exit == 0
    assert "agent-librarian review report" in report_output.out


def test_shell_metacharacters_are_rejected(capsys) -> None:
    exit_code = main(
        [
            "propose",
            "report",
            "examples/generated-catalog; whoami",
        ]
    )

    assert exit_code == 2
    assert "shell control characters" in capsys.readouterr().err


def test_examples_parent_traversal_is_not_inferred_public(capsys) -> None:
    proposal = _proposal(
        ["report", "examples/../private-catalog"],
        capsys,
    )

    assert proposal["sensitivity"] == "unclear"


def test_catalog_arguments_are_limited_to_documented_options() -> None:
    with pytest.raises(SystemExit):
        main(
            [
                "propose",
                "catalog",
                "examples/sample-collection",
                "--out",
                "examples/generated-catalog",
                "--delete-source",
            ]
        )


def test_unclear_and_work_internal_sensitivity_are_blocked(capsys) -> None:
    unclear_path = "private/catalog"
    unclear_command = f"agent-librarian report {unclear_path}"
    unclear_exit = main(
        [
            "run",
            "report",
            unclear_path,
            "--approve-exact",
            unclear_command,
        ]
    )
    unclear_output = capsys.readouterr()

    work_exit = main(
        [
            "run",
            "report",
            unclear_path,
            "--sensitivity",
            "work-internal",
            "--approve-exact",
            unclear_command,
        ]
    )
    work_output = capsys.readouterr()

    assert unclear_exit == 2
    assert "Sensitivity is unclear" in unclear_output.err
    assert work_exit == 2
    assert "blocked for work-internal" in work_output.err


def test_private_local_execution_emits_warning(
    tmp_path: Path,
    capsys,
) -> None:
    catalog_dir = tmp_path / "generated"
    assert _approved_catalog(catalog_dir, capsys) == 0
    exact_command = f"agent-librarian validate {catalog_dir}"

    exit_code = main(
        [
            "run",
            "validate",
            str(catalog_dir),
            "--sensitivity",
            "private-local",
            "--approve-exact",
            exact_command,
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "inherit the source collection's private sensitivity" in captured.err


def test_proposal_state_is_written_only_when_requested(
    tmp_path: Path,
    capsys,
) -> None:
    state_path = tmp_path / "state" / "runtime-state.json"
    _proposal(["report", "examples/generated-catalog"], capsys)
    assert not state_path.exists()

    _proposal(
        [
            "report",
            "examples/generated-catalog",
            "--state-out",
            str(state_path),
        ],
        capsys,
    )

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["workflow_phase"] == "proposal"
    assert state["approval_status"] == "pending"


def test_records_are_explicit_linked_and_do_not_store_source_content(
    tmp_path: Path,
    capsys,
) -> None:
    source = tmp_path / "private-source"
    output = tmp_path / "generated"
    records = tmp_path / "records"
    absent_records = tmp_path / "absent-records"
    source.mkdir()
    (source / "private.md").write_text(
        "# Private fixture\n\nprivate_raw_source_marker\n",
        encoding="utf-8",
    )

    no_records_output = tmp_path / "generated-without-records"
    assert _approved_catalog(no_records_output, capsys) == 0
    assert not absent_records.exists()

    exact_command = f"agent-librarian catalog {source} --out {output}"
    exit_code = main(
        [
            "run",
            "catalog",
            str(source),
            "--out",
            str(output),
            "--sensitivity",
            "private-local",
            "--approve-exact",
            exact_command,
            "--records-out",
            str(records),
        ]
    )
    capsys.readouterr()

    state = json.loads(
        (records / "runtime-state.json").read_text(encoding="utf-8")
    )
    approval = json.loads(
        (records / "approval-log.json").read_text(encoding="utf-8")
    )
    execution = json.loads(
        (records / "execution-record.json").read_text(encoding="utf-8")
    )
    serialized = json.dumps([state, approval, execution])

    assert exit_code == 0
    assert approval["exact_command"] == execution["exact_command"]
    assert state["run_id"] == approval["run_id"] == execution["run_id"]
    assert execution["approval_id"] == approval["approval_id"]
    assert "private_raw_source_marker" not in serialized
    assert "CLI stdout and stderr were emitted" in serialized
