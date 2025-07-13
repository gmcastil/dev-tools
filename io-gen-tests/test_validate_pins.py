import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

pins_test_cases = [
    {
        "id": "valid_pin_array",
        "yaml": """\
title: Pin Array
part: xc7z020clg400-1
signals:
  - name: gpio
    direction: inout
    buffer: ibuf
    pins: [A3, A4, A5, A6]
    bank: 34
    width: 4

        """
        , "valid": True
    },
]

@pytest.mark.parametrize('case', pins_test_cases, ids=[c['id'] for c in pins_test_cases])
def test_validate_pins_test_cases(case):
    if case['valid']:
        validate(yaml.safe_load(case['yaml']))
    else:
        with pytest.raises(ValidationError):
            validate(yaml.safe_load(case['yaml']))