import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

pins_test_cases = [
    # Valid test cases
    {
        "id": "minimal_valid_pins",
        "yaml": """
            title: Minimal Pins
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: in
                buffer: ibuf
                pins: [A1, A2]
        """,
        "valid": True,
    },
    {
        "id": "pins_with_iostandard",
        "yaml": """
            title: Pins With IOStandard
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: out
                buffer: obuf
                pins: [C1, C2, C3]
                iostandard: LVCMOS33
        """,
        "valid": True,
    },
    {
        "id": "pins_with_bank",
        "yaml": """
            title: Pins With Bank
            part: xc7z010clg400-1
            banks:
              - bank: 34
                iostandard: LVCMOS33
                performance: HP
            signals:
              - name: data
                direction: out
                buffer: obuf
                pins: [D1, D2]
                bank: 34
        """,
        "valid": True,
    },
    {
        "id": "pins_with_bank_and_iostandard",
        "yaml": """
            title: Pins With Bank and IOStandard
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: out
                buffer: obuf
                pins: [F1, F2, F3]
                bank: 35
                iostandard: LVCMOS18
        """,
        "valid": True,
    },

    # Invalid test cases
    {
        "id": "pins_too_short",
        "yaml": """
            title: Pins Too Short
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: in
                buffer: ibuf
                pins: [A1]
        """,
        "valid": False,
    },
    {
        "id": "pins_wrong_type_string",
        "yaml": """
            title: Pins As String (Invalid)
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: in
                buffer: ibuf
                pins: A1
        """,
        "valid": False,
    },
    {
        "id": "pins_missing_buffer",
        "yaml": """
            title: Pins Missing Buffer
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: in
                pins: [A1, A2]
        """,
        "valid": False,
    },
    {
        "id": "pins_missing_direction",
        "yaml": """
            title: Pins Missing Direction
            part: xc7z010clg400-1
            signals:
              - name: data
                buffer: ibuf
                pins: [A1, A2]
        """,
        "valid": False,
    },
    {
        "id": "pins_with_extra_field",
        "yaml": """
            title: Pins With Extra Field
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: in
                buffer: ibuf
                pins: [A1, A2]
                foo: bar
        """,
        "valid": False,
    },
    {
        "id": "pins_with_pin_also_present",
        "yaml": """
            title: Pins With Pin Also Present
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: in
                buffer: ibuf
                pin: A1
                pins: [A1, A2]
        """,
        "valid": False,
    }
]

@pytest.mark.parametrize("case", pins_test_cases, ids=[case["id"] for case in pins_test_cases])
def test_validate_pins(case):
    raw_yaml = yaml.safe_load(case["yaml"])
    if case["valid"]:
        validate(raw_yaml)
    else:
        with pytest.raises(ValidationError):
            validate(raw_yaml)

