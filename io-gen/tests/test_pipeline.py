import json
from pathlib import Path

import yaml
from jsonschema.exceptions import ValidationError

from io_gen.signal_table import extract_signal_table
from io_gen.validate_signals import validate_signal_table
from io_gen.validator import validate

# Fixture paths
FIXTURE_YAML = Path("tests/fixtures/pipeline/integration.yaml")
FIXTURE_SIG_TABLE = Path("tests/fixtures/pipeline/integration.signal_table.json")


def test_pipeline():
    # Load YAML
    with open(FIXTURE_YAML) as f:
        data = yaml.safe_load(f)

    # Stage 1: Schema validation
    try:
        validate(data)
    except ValidationError as e:
        print("Validation failed!")
        print("Path:", list(e.path))
        print("Message:", e.message)
        print("Schema path:", list(e.schema_path))
        raise

    # Stage 2: Signal table extraction
    try:
        signal_table = extract_signal_table(data["signals"])
    except ValueError as e:
        print("Signal table extraction failed!")
        raise

    validate_signal_table(signal_table)

    # Load expected signal table
    with open(FIXTURE_SIG_TABLE) as f:
        expected = json.load(f)

    # Compare
    assert signal_table == expected
