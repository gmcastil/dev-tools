import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

pinset_test_cases = [
    # Scalar pinset
    {
        "id": "scalar_pinset_valid",
        "yaml": """
            title: Scalar Pinset
            part: xc7z010clg400-1
            signals:
              - name: clk_diff
                direction: in
                buffer: ibufds
                pinset:
                  p: A1
                  n: A2
        """,
        "valid": True,
    },

    # Bus of differential pairs
    {
        "id": "bus_pinset_valid",
        "yaml": """
            title: Bus Pinset
            part: xc7z010clg400-1
            signals:
              - name: lvds_data
                direction: in
                buffer: ibufds
                pinset:
                  p: [A1, A2]
                  n: [B1, B2]
        """,
        "valid": True,
    },

    # Mixed differential p and n (one string, one list)
    {
        "id": "pinset_mixed_types",
        "yaml": """
            title: Mixed Pinset Types
            part: xc7z010clg400-1
            signals:
              - name: lvds_data
                direction: in
                buffer: ibufds
                pinset:
                  p: A1
                  n: [B1, B2]
        """,
        "valid": False,
    },

    # Missing pin of pinset (n)
    {
        "id": "pinset_missing_n",
        "yaml": """
            title: Missing N
            part: xc7z010clg400-1
            signals:
              - name: clk_diff
                direction: in
                buffer: ibufds
                pinset:
                  p: A1
        """,
        "valid": False,
    },

    # Missing pin of pinset (p)
    {
        "id": "pinset_missing_p",
        "yaml": """
            title: Missing P
            part: xc7z010clg400-1
            signals:
              - name: clk_diff
                direction: in
                buffer: ibufds
                pinset:
                  n: A2
        """,
        "valid": False,
    },

    # Extra field
    {
        "id": "pinset_extra_field",
        "yaml": """
            title: Extra Field in Pinset
            part: xc7z010clg400-1
            signals:
              - name: clk_diff
                direction: in
                buffer: ibufds
                pinset:
                  p: A1
                  n: A2
                  extra: junk
        """,
        "valid": False,
    },

    # List of pins too short and mismatched
    {
        "id": "pinset_bus_too_short_mismatched",
        "yaml": """
            title: Too Short Bus
            part: xc7z010clg400-1
            signals:
              - name: lvds_data
                direction: in
                buffer: ibufds
                pinset:
                  p: [A1 A2]
                  n: [B1]
        """,
        "valid": False,
    },

    # List of pins too short
    {
        "id": "pinset_bus_too_short",
        "yaml": """
            title: Too Short Bus
            part: xc7z010clg400-1
            signals:
              - name: lvds_data
                direction: in
                buffer: ibufds
                pinset:
                  p: [A1]
                  n: [B1]
        """,
        "valid": False,
    }
]

@pytest.mark.parametrize("case", pinset_test_cases, ids=[case["id"] for case in pinset_test_cases])
def test_validate_pinset(case):
    raw_yaml = yaml.safe_load(case["yaml"])
    if case["valid"]:
        validate(raw_yaml)
    else:
        with pytest.raises(ValidationError):
            validate(raw_yaml)

