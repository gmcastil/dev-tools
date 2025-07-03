"""
Tests for schema-level validation (presence of required fields, disallowed extras, etc).

"""

import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

pin_test_cases = [
    # Valid test cases
    {
        "id": "minimal_valid_pin",
        "yaml": """
            title: Minimal Pin
            part: xc7z010clg400-1
            signals:
              - name: reset
                direction: in
                buffer: ibuf
                pin: A1
        """,
        "valid": True,
    },
    {
        "id": "pin_with_bank",
        "yaml": """
            title: Pin with Bank
            part: xc7z010clg400-1
            banks:
              - bank: 34
                iostandard: LVCMOS33
                performance: HP
            signals:
              - name: reset
                direction: in
                buffer: ibuf
                pin: A1
                bank: 34
        """,
        "valid": True,
    },
    {
        "id": "pin_with_iostandard",
        "yaml": """
            title: Pin with IOStandard
            part: xc7z010clg400-1
            signals:
              - name: reset
                direction: in
                buffer: ibuf
                pin: A1
                iostandard: LVCMOS33
        """,
        "valid": True,
    },
    {
        "id": "pin_with_bank_and_iostd",
        "yaml": """
            title: Pin with Bank and IOStandard
            part: xc7z010clg400-1
            signals:
              - name: reset
                direction: in
                buffer: ibuf
                pin: A1
                bank: 34
                iostandard: LVCMOS33
        """,
        "valid": True,
    },

    # Invalid test cases
    {
        "id": "missing_pin",
        "yaml": """
            title: Missing Pin Field
            part: xc7z010clg400-1
            signals:
              - name: reset
                direction: in
                buffer: ibuf
                # pin is missing
        """,
        "valid": False,
    },
    {
        "id": "pin_wrong_type_list",
        "yaml": """
            title: Pin as List (Invalid)
            part: xc7z010clg400-1
            signals:
              - name: reset
                direction: in
                buffer: ibuf
                pin: [A1]
        """,
        "valid": False,
    },
    {
        "id": "pin_wrong_type_number",
        "yaml": """
            title: Pin as Number (Invalid)
            part: xc7z010clg400-1
            signals:
              - name: reset
                direction: in
                buffer: ibuf
                pin: 42
        """,
        "valid": False,
    },
    {
        "id": "missing_buffer",
        "yaml": """
            title: Missing Buffer
            part: xc7z010clg400-1
            signals:
              - name: reset
                direction: in
                pin: A1
        """,
        "valid": False,
    },
    {
        "id": "missing_direction",
        "yaml": """
            title: Missing Direction
            part: xc7z010clg400-1
            signals:
              - name: reset
                buffer: ibuf
                pin: A1
        """,
        "valid": False,
    },
    {
        "id": "missing_name",
        "yaml": """
            title: Missing Name
            part: xc7z010clg400-1
            signals:
              - direction: in
                buffer: ibuf
                pin: A1
        """,
        "valid": False,
    },
    {
        "id": "extra_field_on_signal",
        "yaml": """
            title: Extra Field
            part: xc7z010clg400-1
            signals:
              - name: reset
                direction: in
                buffer: ibuf
                pin: A1
                unexpected: true
        """,
        "valid": False,
    },
    {
        "id": "pin_with_too_many_fields",
        "yaml": """
            title: Pin with Pin and Pins (Invalid)
            part: xc7z010clg400-1
            signals:
              - name: reset
                direction: in
                buffer: ibuf
                pin: A1
                pins: [A1]
        """,
        "valid": False,
    },
]

@pytest.mark.parametrize("case", pin_test_cases, ids=[case["id"] for case in pin_test_cases])
def test_validate_pin(case):
    raw_yaml = yaml.safe_load(case["yaml"])
    if case["valid"]:
        validate(raw_yaml)
    else:
        with pytest.raises(ValidationError):
            validate(raw_yaml)
