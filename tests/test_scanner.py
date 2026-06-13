from pathlib import Path

from agent_librarian.scanner import scan_files


def test_scanner_excludes_common_and_output_directories(tmp_path: Path) -> None:
    root = tmp_path / "collection"
    output = root / "generated"
    included = root / "skills" / "demo" / "SKILL.md"
    ignored = [
        root / ".git" / "config.json",
        root / ".venv" / "settings.yaml",
        root / "node_modules" / "package.json",
        root / "__pycache__" / "cache.json",
        output / "index.json",
    ]
    included.parent.mkdir(parents=True)
    included.write_text("# Demo", encoding="utf-8")
    for path in ignored:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}", encoding="utf-8")
    (root / "notes.txt").write_text("unsupported", encoding="utf-8")

    found = scan_files(root, output)

    assert found == [included]
