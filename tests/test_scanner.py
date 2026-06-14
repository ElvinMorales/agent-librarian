from pathlib import Path

from agent_librarian.scanner import scan_file_inventory, scan_files


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


def test_default_inventory_includes_supported_and_unsupported_files(
    tmp_path: Path,
) -> None:
    root = tmp_path / "collection"
    markdown = root / "README.md"
    yaml = root / "agent.yaml"
    unsupported = root / "notes.txt"
    root.mkdir()
    markdown.write_text("# Demo", encoding="utf-8")
    yaml.write_text("name: demo", encoding="utf-8")
    unsupported.write_text("notes", encoding="utf-8")

    assert scan_file_inventory(root) == [markdown, yaml, unsupported]


def test_include_patterns_narrow_inventory_and_support_multiple_patterns(
    tmp_path: Path,
) -> None:
    root = tmp_path / "collection"
    markdown = root / "README.md"
    nested_markdown = root / "skills" / "SKILL.md"
    yaml = root / "agent.yaml"
    json_file = root / "agent.json"
    nested_markdown.parent.mkdir(parents=True)
    markdown.write_text("# Demo", encoding="utf-8")
    nested_markdown.write_text("# Skill", encoding="utf-8")
    yaml.write_text("name: demo", encoding="utf-8")
    json_file.write_text("{}", encoding="utf-8")

    markdown_only = scan_file_inventory(root, include_patterns=["**/*.md"])
    markdown_and_yaml = scan_file_inventory(
        root, include_patterns=["**/*.md", "**/*.yaml"]
    )

    assert markdown_only == [markdown, nested_markdown]
    assert markdown_and_yaml == [markdown, yaml, nested_markdown]


def test_custom_excludes_support_names_repetition_and_comma_separated_values(
    tmp_path: Path,
) -> None:
    root = tmp_path / "collection"
    included = root / "public" / "README.md"
    excluded = [
        root / "private" / "secret.md",
        root / "scratch" / "draft.md",
        root / "tmp" / "cache.json",
        root / "nested" / "private" / "notes.yaml",
    ]
    included.parent.mkdir(parents=True)
    included.write_text("# Public", encoding="utf-8")
    for path in excluded:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("private_contents_marker", encoding="utf-8")

    found = scan_file_inventory(root, exclude_patterns=["private", " scratch, tmp "])

    assert found == [included]


def test_custom_excludes_preserve_safe_default_excludes(tmp_path: Path) -> None:
    root = tmp_path / "collection"
    included = root / "public" / "README.md"
    excluded = [
        root / "private" / "secret.md",
        root / ".git" / "config.json",
        root / ".env",
        root / "venv" / "settings.yaml",
        root / ".pytest_cache" / "cache.json",
        root / ".mypy_cache" / "cache.json",
        root / ".ruff_cache" / "cache.json",
        root / "dist" / "manifest.json",
        root / "build" / "manifest.json",
        root / "examples" / "generated-catalog" / "index.json",
    ]
    included.parent.mkdir(parents=True)
    included.write_text("# Public", encoding="utf-8")
    for path in excluded:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("private_contents_marker", encoding="utf-8")

    assert scan_file_inventory(root, exclude_patterns=["private"]) == [included]


def test_output_directory_under_input_root_is_excluded(tmp_path: Path) -> None:
    root = tmp_path / "collection"
    output = root / "custom-output"
    included = root / "README.md"
    generated = output / "index.json"
    output.mkdir(parents=True)
    included.write_text("# Public", encoding="utf-8")
    generated.write_text('{"private": "private_contents_marker"}', encoding="utf-8")

    assert scan_file_inventory(root, output) == [included]
