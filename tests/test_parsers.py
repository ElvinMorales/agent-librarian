from pathlib import Path

from agent_librarian.parsers import parse_artifact


def test_markdown_parser_extracts_frontmatter_and_headings(tmp_path: Path) -> None:
    skill = tmp_path / "skills" / "demo" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        """---
name: Demo Skill
description: Produce a deterministic demonstration result.
tags: [demo, test]
---
# Ignored Fallback

## Purpose
Show structured extraction.

## When to use
- A parser test needs a fixture.

## Inputs
- Example text.

## Outputs
- Example result with findings, citations, and open questions.
""",
        encoding="utf-8",
    )

    entry = parse_artifact(skill, tmp_path)

    assert entry.name == "Demo Skill"
    assert entry.artifact_type == "capability_module"
    assert entry.taxonomy_bucket == "Capability modules"
    assert entry.purpose == "Show structured extraction."
    assert entry.activation_triggers == ["A parser test needs a fixture."]
    assert entry.inputs == ["Example text."]
    assert entry.outputs == [
        "Example result with findings, citations, and open questions."
    ]
    assert entry.tags == ["demo", "test"]
    assert entry.extraction["confidence"] == 1.0


def test_json_parser_recognizes_mcp_style_manifest(tmp_path: Path) -> None:
    manifest = tmp_path / "mcp" / "sample-server.json"
    manifest.parent.mkdir()
    manifest.write_text(
        '{"name":"sample","protocol":"mcp","mcpServers":{}}',
        encoding="utf-8",
    )

    entry = parse_artifact(manifest, tmp_path)

    assert entry.artifact_type == "protocol_manifest"
    assert entry.framework_hint == "MCP"
