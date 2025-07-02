import pytest
import yaml
from io_gen.validator import validate

# Define test cases in a single dictionary
invalid_schema_cases = {
    "missing_required_field_part": {
        "yaml": """
title: MissingPart
banks: []
signals: []
""",
        "error": "part"
    },

    "invalid_direction_enum": {
        "yaml": """
title: BadDir
part: xc7z010clg400-1
banks:
  - bank: 34
    iostandard: LVCMOS33
    performance: HR
signals:
  - name: foo
    direction: invalid
    buffer: ibuf
    bank: 34
    pin: "A1"
""",
        "error": "is not one of"
    },

    "signal_missing_pin_shape": {
        "yaml": """
title: MissingPins
part: xc7z010clg400-1
banks:
  - bank: 34
    iostandard: LVCMOS33
    performance: HR
signals:
  - name: bad
    direction: out
    buffer: obuf
    bank: 34
    # missing pin/pins/pinset
""",
        "error": "oneOf"
    },

    "bad_pinset_mixed_types": {
        "yaml": """
title: PinsetMix
part: xc7z010clg400-1
banks:
  - bank: 34
    iostandard: LVDS
    performance: HR
signals:
  - name: mixed
    direction: in
    buffer: ibufds
    bank: 34
    pinset:
      p: ["A1", "A2"]
      n: "B1"  # mixed types!
""",
        "error": "oneOf"
    }
}


# One test function to rule them all
@pytest.mark.parametrize("name,test", invalid_schema_cases.items())
def test_invalid_schema_cases(name, test):
    with pytest.raises(Exception, match=test["error"]):
        data = yaml.safe_load(test["yaml"])
        validate(data)

