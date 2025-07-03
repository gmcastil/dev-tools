import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

banks_test_cases = [
    # Valid cases
    {
        "id": "valid_bank_entry",
        "yaml": """
            title: Valid Banks
            part: xc7z010clg400-1
            banks:
              - bank: 34
                iostandard: LVCMOS33
                performance: HR
              - bank: 35
                iostandard: LVCMOS18
                performance: HP
            signals:
              - name: dummy
                direction: in
                buffer: ibuf
                pin: A1
                iostandard: LVCMOS33
        """,
        "valid": True,
    },

    # Unknown IOSTANDARD
    {
        "id": "missing_performance",
        "yaml": """
            title: Missing Performance Field
            part: xc7z010clg400-1
            banks:
              - bank: 34
                iostandard: UNKNOWN
                performance: HP
            signals:
              - name: dummy
                direction: in
                buffer: ibuf
                pin: A1
                iostandard: LVCMOS33
        """,
        "valid": False,
    },
    # Missing performance
    {
        "id": "missing_performance",
        "yaml": """
            title: Missing Performance Field
            part: xc7z010clg400-1
            banks:
              - bank: 34
                iostandard: LVCMOS33
            signals:
              - name: dummy
                direction: in
                buffer: ibuf
                pin: A1
                iostandard: LVCMOS33
        """,
        "valid": False,
    },

    # Unknown field in bank
    {
        "id": "extra_field_in_bank",
        "yaml": """
            title: Extra Field In Bank
            part: xc7z010clg400-1
            banks:
              - bank: 34
                iostandard: LVCMOS33
                performance: HR
                pizza: true
            signals:
              - name: dummy
                direction: in
                buffer: ibuf
                pin: A1
                iostandard: LVCMOS33
        """,
        "valid": False,
    },

    # Wrong type for bank number
    {
        "id": "bank_number_as_string",
        "yaml": """
            title: Bank Number As String
            part: xc7z010clg400-1
            banks:
              - bank: "34"
                iostandard: LVCMOS33
                performance: HR
            signals:
              - name: dummy
                direction: in
                buffer: ibuf
                pin: A1
                iostandard: LVCMOS33
        """,
        "valid": False,
    }
]

@pytest.mark.parametrize("case", banks_test_cases, ids=[case["id"] for case in banks_test_cases])
def test_validate_banks(case):
    raw_yaml = yaml.safe_load(case["yaml"])
    if case["valid"]:
        validate(raw_yaml)
    else:
        with pytest.raises(ValidationError):
            validate(raw_yaml)

