import pytest
from copy import deepcopy

from io_gen.flatten import flatten_pins
from tests.utils import assert_flat_signals_equal

pins_test_cases = [
    {
        "id": "valid_pins_inherits_iostandard",
        "valid": True,
        "signal": {
            "name": "data",
            "direction": "in",
            "buffer": "ibuf",
            "pins": ["A1", "A2", "A3"],
            "bank": 34
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"}
        },
        "expected": [
            {
                "name": "data",
                "index": 0,
                "pin": "A1",
                "bank": 34,
                "direction": "in",
                "buffer": "ibuf",
                "as_bus": False,
                "iostandard": "LVCMOS33"
            },
            {
                "name": "data",
                "index": 1,
                "pin": "A2",
                "bank": 34,
                "direction": "in",
                "buffer": "ibuf",
                "as_bus": False,
                "iostandard": "LVCMOS33"
            },
            {
                "name": "data",
                "index": 2,
                "pin": "A3",
                "bank": 34,
                "direction": "in",
                "buffer": "ibuf",
                "as_bus": False,
                "iostandard": "LVCMOS33"
            }
        ]
    },
    {
        "id": "valid_pins_explicit_iostandard",
        "valid": True,
        "signal": {
            "name": "data",
            "direction": "out",
            "buffer": "obuf",
            "pins": ["B1", "B2"],
            "bank": 35,
            "iostandard": "SSTL15"
        },
        "banks": {
            35: {"iostandard": "LVCMOS18"}
        },
        "expected": [
            {
                "name": "data",
                "index": 0,
                "pin": "B1",
                "bank": 35,
                "direction": "out",
                "buffer": "obuf",
                "as_bus": False,
                "iostandard": "SSTL15"
            },
            {
                "name": "data",
                "index": 1,
                "pin": "B2",
                "bank": 35,
                "direction": "out",
                "buffer": "obuf",
                "as_bus": False,
                "iostandard": "SSTL15"
            }
        ]
    },
    {
        "id": "missing_pins_field_should_fail",
        "valid": False,
        "signal": {
            "name": "foo",
            "direction": "in",
            "buffer": "ibuf",
            "bank": 34
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"}
        }
    },
    {
        "id": "missing_bank_should_fail",
        "valid": False,
        "signal": {
            "name": "bar",
            "direction": "in",
            "buffer": "ibuf",
            "pins": ["C1", "C2"],
            "bank": 99
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"}
        }
    }
]

test_ids = [c["id"] for c in pins_test_cases]

@pytest.mark.parametrize("case", pins_test_cases, ids=test_ids)
def test_flatten_pins_cases(case):
    signal = deepcopy(case["signal"])
    banks = case['banks']

    if case["valid"]:
        result = flatten_pins(signal, banks)
        assert_flat_signals_equal(result, case['expected'])
    else:
        with pytest.raises(Exception):
            flatten_pins(case["signal"], case["banks"])
