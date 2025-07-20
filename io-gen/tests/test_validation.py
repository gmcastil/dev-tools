import pytest
import yaml
from pathlib import Path
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

FIXTURE_DIR = Path("tests/fixtures/schema")


def load_yaml_file(path):
    with open(path) as f:
        return yaml.safe_load(f)


@pytest.mark.parametrize(
    "filename,should_pass",
    [
        ("valid-bus.yaml", True),
        ("valid-pinset-bus.yaml", True),
        ("valid-scalar.yaml", True),
        ("valid-multibank.yaml", True),
        ("valid-pinset-scalar.yaml", True),
        ("valid-scalar-with-width.yaml", True),
        ("invalid-missing-direction.yaml", False),
        ("invalid-pinset-array-no-width.yaml", False),
        ("invalid-unknown-field.yaml", False),
        ("invalid-multibank-no-width.yaml", False),
        ("valid-generate-false.yaml", True),
        ("valid-multibank-pin.yaml", True),
        ("invalid-mixed-pins-pinset.yaml", False),
        ("invalid-missing-io-type.yaml", False),
        ("invalid-pinset-bus-missing-width.yaml", False),
        ("invalid-multibank-missing-offset.yaml", False),
        ("invalid-bank-missing-iostandard.yaml", False),
        ("invalid-multibank-extra-fields.yaml", False),
    ],
)
def test_schema_validation(filename, should_pass):
    data = load_yaml_file(FIXTURE_DIR / filename)

    print(data["signals"][0])
    if should_pass:
        validate(data)
    else:
        with pytest.raises(ValidationError):
            validate(data)
