import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

bank_test_cases = [
    {
        "id": "valid_banks_minimal",
        "yaml": """
title: Bank Table Test
part: xc7z010clg400-1
banks:
  34:
    iostandard: LVCMOS33
    performance: HD
  35:
    iostandard: LVDS
    performance: HR
signals:
  - name: dummy
    pin: A1
    direction: out
    buffer: obuf
    bank: 34
        """,
        "valid": True,
    },
    {
        "id": "valid_banks_with_comments",
        "yaml": """
title: Bank Table with Comments
part: xc7z010clg400-1
banks:
  34:
    iostandard: LVCMOS33
    performance: HD
    comment: "For GPIO"
  35:
    iostandard: LVDS_25
    performance: HR
    comment: "Diff pair bank"
signals:
  - name: dummy
    pin: A1
    direction: out
    buffer: obuf
    bank: 34
        """,
        "valid": True,
    },
    {
        "id": "invalid_bank_missing_iostandard",
        "yaml": """
title: Bank Missing iostandard
part: xc7z010clg400-1
banks:
  34:
    performance: HD
signals:
  - name: dummy
    pin: A1
    direction: out
    buffer: obuf
    bank: 34
        """,
        "valid": False,
    },
    {
        "id": "invalid_bank_with_extra_field",
        "yaml": """
title: Bank With Extra Field
part: xc7z010clg400-1
banks:
  34:
    iostandard: LVCMOS33
    performance: HD
    foo: bar
signals:
  - name: dummy
    pin: A1
    direction: out
    buffer: obuf
    bank: 34
        """,
        "valid": False,
    }
]

@pytest.mark.parametrize('case', bank_test_cases, ids=[c["id"] for c in bank_test_cases])
def test_validate_bank_table(case):
    if case["valid"]:
        validate(yaml.safe_load(case["yaml"]))
    else:
        with pytest.raises(ValidationError):
            validate(yaml.safe_load(case["yaml"]))
