"""
Validate input data before processing
"""
import json
from pathlib import Path
from typing import List, Dict, Any

from referencing import Registry, Resource
from jsonschema.exceptions import ValidationError
from jsonschema import Draft202012Validator

# Schema locations
SCHEMA_DIR = Path(__file__).parent.parent / "schema"
SCHEMA_PATH = SCHEMA_DIR / "schema.json"
DEFS_DIR = SCHEMA_DIR / "defs"

with open(SCHEMA_PATH) as f:
    io_gen_base_schema = json.load(f)

defs = {
        "defs/iostandard.json": json.load((DEFS_DIR / "iostandard.json").open()),
        "defs/buffer.json": json.load((DEFS_DIR / "buffer.json").open()),
        "defs/direction.json": json.load((DEFS_DIR / "direction.json").open()),
        "defs/group.json": json.load((DEFS_DIR / "group.json").open()),
        "defs/bank.json": json.load((DEFS_DIR / "bank.json").open()),
        "defs/performance.json": json.load((DEFS_DIR / "performance.json").open()),
        "defs/pin.json": json.load((DEFS_DIR / "pin.json").open()),
        "defs/pins.json": json.load((DEFS_DIR / "pins.json").open()),
        "defs/pinset.json": json.load((DEFS_DIR / "pinset.json").open()),
        "defs/multibank.json": json.load((DEFS_DIR / "multibank.json").open())
}

resources = {
        "schema.json": Resource.from_contents(io_gen_base_schema),
        **{key: Resource.from_contents(value) for key, value in defs.items()}
}

registry = Registry().with_resources(resources.items())

validator = Draft202012Validator(io_gen_base_schema, registry=registry)

def validate(data: dict) -> None:
    """
    Validate the given YAML-parsed dictionary against the IO schema.

    Args:
        data: A dictionary loaded from a YAML file using yaml.safe_load().

    Raises:
        jsonschema.exceptions.ValidationError: If the data does not conform to the schema.

    """
    validator.validate(data)

def load_enum_values(schema_path: Path) -> List[str]:
    """Load the list of enum values from a JSON schema fragment.

    Useful for getting the enumerated values like IOSTANDARD, buffer types, directions,
    from JSON into Python without having to hard code values (and breaking tests when
    the supported types and so forth change).

    Args:
        schema_path: Path to a schema file with an "enum" key.

    Returns:
        A list of allowed enum values.

    Raises:
        ValueError: If the file doesn't contain an 'enum' key.

    """
    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    if "enum" not in schema:
        raise ValueError(f"Schema {schema_path} has no 'enum' key.")

    values = schema["enum"]
    if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
        raise ValueError(f"Invalid enum contents in {schema_path}: {values}")

    return values

