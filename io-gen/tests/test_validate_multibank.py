import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

multibank_test_cases = [
    # VALID: two banks, split with pins
    {
        "id": "multibank_split_pins",
        "yaml": """
            title: Split Pins Across Banks
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: out
                buffer: obuf
                width: 4
                multibank:
                  - bank: 34
                    pins: [A1, A2]
                    offset: 0
                  - bank: 35
                    pins: [B1, B2]
                    offset: 2
        """,
        "valid": True,
    },

    {
        "id": "multibank_split_pins",
        "yaml": """
            title: Split Pins Across Banks
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: out
                buffer: obuf
                width: 5
                multibank:
                  - bank: 34
                    pins: [A1, A2]
                    offset: 0
                  - bank: 35
                    pins: [A3, A4, A5]
                    offset: 2
        """,
        "valid": True,
    },

    # VALID: mix of pin and pins
    {
        "id": "multibank_pin_and_pins",
        "yaml": """
            title: Mixed Pin Forms
            part: xc7z010clg400-1
            signals:
              - name: ctrl
                direction: out
                buffer: obuf
                width: 3
                multibank:
                  - bank: 34
                    pin: A1
                    offset: 0
                  - bank: 35
                    pins: [B1, B2]
                    offset: 1
        """,
        "valid": True,
    },

    # VALID: bus differential pair
    {
        "id": "multibank_pinset_bus",
        "yaml": """
            title: Bus Diff Pair
            part: xc7z010clg400-1
            signals:
              - name: lvds
                direction: in
                buffer: ibufds
                width: 4
                multibank:
                  - bank: 34
                    pinset:
                      p: [A1, A2]
                      n: [B1, B2]
                    offset: 0
                  - bank: 35
                    pinset:
                      p: [C1, C2]
                      n: [D1, D2]
                    offset: 2
        """,
        "valid": True,
    },

    # INVALID: missing bank
    {
        "id": "multibank_missing_bank",
        "yaml": """
            title: Missing Bank
            part: xc7z010clg400-1
            signals:
              - name: bad
                direction: in
                buffer: ibuf
                width: 4
                multibank:
                  - pins: [A1, A2]
                    offset: 0
                  - bank: 35
                    pins: [B1, B2]
                    offset: 2
        """,
        "valid": False,
    },

    # INVALID: no pin/pins/pinset
    {
        "id": "multibank_no_pin_form",
        "yaml": """
            title: No Pins Given
            part: xc7z010clg400-1
            signals:
              - name: bad
                direction: in
                buffer: ibuf
                width: 3
                multibank:
                  - bank: 34
                    offset: 0
                  - bank: 35
                    offset: 2
        """,
        "valid": False,
    },

    # INVALID: extra field
    {
        "id": "multibank_extra_field",
        "yaml": """
            title: Extra Field
            part: xc7z010clg400-1
            signals:
              - name: data
                direction: out
                buffer: obuf
                width: 4
                multibank:
                  - bank: 34
                    pins: [A1, A2]
                    offset: 0
                    foo: bar
                  - bank: 35
                    pins: [B1, B2]
                    offset: 2
        """,
        "valid": False,
    },

    # INVALID: missing width
    {
        "id": "multibank_missing_width",
        "yaml": """
            title: "Missing width test"
            part: "xc7z020"
            signals:
              - name: data_bus
                direction: in
                buffer: ibuf
                multibank:
                  - bank: 34
                    pins: [A1, A2]
                    offset: 0
                  - bank: 35
                    pins: [A3, A4]
                    offset: 21
        """,
        "valid": False,
    }
]

@pytest.mark.parametrize("case", multibank_test_cases, ids=[case["id"] for case in multibank_test_cases])
def test_validate_multibank(case):
    raw_yaml = yaml.safe_load(case["yaml"])
    if case["valid"]:
        validate(raw_yaml)
    else:
        with pytest.raises(ValidationError):
            validate(raw_yaml)

