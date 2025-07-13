import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

pin_test_cases = [
    {
        "id": "valid_scalar_pin_as_bus",
        "yaml": """
title: Scalar Pin with as_bus
part: xc7z020clg400-1
signals:
  - name: reset_n
    direction: in
    buffer: ibuf
    pins: A1
    bank: 34
    as_bus: true
        """
        , "valid": True
    },
    {
        "id": "valid_scalar_pin_no_as_bus",
        "yaml": """
title: Scalar Pin no as_bus
part: xc7z020clg400-1
signals:
  - name: led0
    direction: out
    buffer: obuf
    pins: A2
    bank: 34
    as_bus: false
        """
        , "valid": True
    },
]

@pytest.mark.parametrize('case', pin_test_cases, ids=[c['id'] for c in pin_test_cases])
def test_validate_pin_test_cases(case):
    if case['valid']:
        validate(yaml.safe_load(case['yaml']))
    else:
        with pytest.raises(ValidationError):
            validate(yaml.safe_load(case['yaml']))
