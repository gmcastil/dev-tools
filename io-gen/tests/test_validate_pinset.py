import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

pinset_test_cases = [
    {
        "id": "valid_scalar_pinset",
        "yaml": """
title: Scalar Pinset
part: xc7z020clg400-1
signals:
  - name: clk_diff
    direction: in
    buffer: ibufds
    pinset:
      p: B1
      n: B2
    bank: 35
    as_bus: false
        """
        , "valid": True
    },
    {
        "id": "valid_array_pinset",
        "yaml": """
title: Array Pinset
part: xc7z020clg400-1
signals:
  - name: diff_data
    direction: in
    buffer: ibufds
    pinset:
      p: [B3, B5]
      n: [B4, B6]
    bank: 35
    width: 2
        """
        , "valid": True
    },
]

@pytest.mark.parametrize('case', pinset_test_cases, ids=[c['id'] for c in pinset_test_cases])
def test_validate_pinset_test_cases(case):
    if case['valid']:
        validate(yaml.safe_load(case['yaml']))
    else:
        with pytest.raises(ValidationError):
            validate(yaml.safe_load(case['yaml']))