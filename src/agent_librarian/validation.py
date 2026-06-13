from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import FormatChecker
from jsonschema.exceptions import best_match
from jsonschema.validators import validator_for
from referencing import Registry, Resource


SCHEMA_FILES = (
    "catalog-index.schema.json",
    "catalog-entry.schema.json",
    "overlap-report.schema.json",
    "diagnostics.schema.json",
)

CATALOG_FILES = (
    ("index.json", "catalog-index.schema.json"),
    ("overlap-report.json", "overlap-report.schema.json"),
    ("diagnostics.json", "diagnostics.schema.json"),
)


@dataclass(frozen=True)
class ValidationResult:
    file_name: str
    valid: bool
    message: str


def validate_catalog(catalog_dir: Path) -> list[ValidationResult]:
    schemas = _load_schemas()
    registry = Registry().with_resources(
        [
            (schema["$id"], Resource.from_contents(schema))
            for schema in schemas.values()
        ]
    )

    results = []
    for file_name, schema_name in CATALOG_FILES:
        path = catalog_dir / file_name
        if not path.is_file():
            results.append(ValidationResult(file_name, False, "file is missing"))
            continue

        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            results.append(
                ValidationResult(
                    file_name,
                    False,
                    f"invalid JSON at line {exc.lineno}, column {exc.colno}",
                )
            )
            continue
        except (OSError, UnicodeError) as exc:
            results.append(ValidationResult(file_name, False, str(exc)))
            continue

        schema = schemas[schema_name]
        validator_class = validator_for(schema)
        validator_class.check_schema(schema)
        validator = validator_class(
            schema,
            registry=registry,
            format_checker=FormatChecker(),
        )
        error = best_match(validator.iter_errors(document))
        if error is None:
            results.append(ValidationResult(file_name, True, "schema valid"))
        else:
            results.append(
                ValidationResult(
                    file_name,
                    False,
                    f"{_format_json_path(error.absolute_path)}: {error.message}",
                )
            )
    return results


def _load_schemas() -> dict[str, dict[str, Any]]:
    schema_root = resources.files("agent_librarian").joinpath("schema_data")
    schemas = {}
    for file_name in SCHEMA_FILES:
        schema = json.loads(schema_root.joinpath(file_name).read_text(encoding="utf-8"))
        schemas[file_name] = schema
    return schemas


def _format_json_path(path: Any) -> str:
    formatted = "$"
    for part in path:
        if isinstance(part, int):
            formatted += f"[{part}]"
        else:
            formatted += f".{part}"
    return formatted
