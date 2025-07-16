import yaml
import json
from pathlib import Path
from io_gen.validator import validate
from io_gen.signal_table import extract_signal_table

from jsonschema.exceptions import ValidationError

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
        print("Path:", list(e.path))            # Points to the failing object (e.g. ['signals', 2, 'comment', 'hdl'])
        print("Message:", e.message)            # Human-readable error
        print("Schema path:", list(e.schema_path))  # Which rule failed
        raise

    # Stage 2: Generate signal table from validated data, and compare with actual from JSON
    try:
        sig_table = extract_signal_table(data['signals'])
    except ValueError as e:
        print("Signal table extraction failed!")
        raise

    with open(FIXTURE_SIG_TABLE) as f:
        expected_table = json.load(f)

    compare_signal_tables(sig_table, expected_table)

def compare_signal_tables(actual: dict, expected: dict):
    missing_keys = set(expected) - set(actual)
    extra_keys = set(actual) - set(expected)

    if missing_keys or extra_keys:
        msg = []
        if missing_keys:
            msg.append(f"Missing keys in actual: {sorted(missing_keys)}")
        if extra_keys:
            msg.append(f"Unexpected keys in actual: {sorted(extra_keys)}")
        raise AssertionError("\n".join(msg))

    for signal in sorted(expected):
        actual_entry = actual[signal]
        expected_entry = expected[signal]

        # Compare field-by-field
        for field in expected_entry:
            if field not in actual_entry:
                raise AssertionError(f"Signal '{signal}' is missing field '{field}' in actual.")
            if actual_entry[field] != expected_entry[field]:
                raise AssertionError(
                    f"Signal '{signal}' field '{field}' mismatch:\n"
                    f"  Expected: {expected_entry[field]!r}\n"
                    f"  Actual:   {actual_entry[field]!r}"
                )

        # Extra fields in actual (not expected)
        for field in actual_entry:
            if field not in expected_entry:
                raise AssertionError(
                    f"Signal '{signal}' has unexpected field '{field}' in actual."
                )
