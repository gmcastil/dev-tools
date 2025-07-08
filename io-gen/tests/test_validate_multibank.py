import pytest
import yaml
from io_gen.validator import validate
from jsonschema.exceptions import ValidationError

multibank_test_cases = [
    {
        "id": "valid_multibank_pins",
        "yaml": """
title: Multibank Pins
part: xc7z020clg400-1
signals:
  - name: data_bus
    direction: out
    buffer: obuf
    width: 4
    multibank:
      - bank: 34
        pins: [C1, C2]
        offset: 0
      - bank: 36
        pins: [D1, D2]
        offset: 2
        """
        , "valid": True
    },
    {
        "id": "valid_multibank_diff",
        "yaml": """
title: Multibank Differential
part: xc7z020clg400-1
signals:
  - name: sync_diff
    direction: out
    buffer: obufds
    width: 2
    multibank:
      - bank: 35
        pinset:
          p: F1
          n: F2
        offset: 0
      - bank: 35
        pinset:
          p: F3
          n: F4
        offset: 1
        """
        , "valid": True
    },
]

@pytest.mark.parametrize('case', multibank_test_cases, ids=[c['id'] for c in multibank_test_cases])
def test_validate_multibank_test_cases(case):
    if case['valid']:
        validate(yaml.safe_load(case['yaml']))
    else:
        with pytest.raises(ValidationError):
            validate(yaml.safe_load(case['yaml']))