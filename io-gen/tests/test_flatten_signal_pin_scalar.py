import pytest
from io_gen.pin_table import flatten_signal_pin_scalar

from tests.utils import assert_flat_signals_equal

cases = [
    {
        "id": "scalar-pin-valid",
        "signal": {
            "name": "led",
            "pin": "A1",
            "bank": 34,
            "direction": "out",
            "buffer": "obuf"
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"}
        },
        "expected": [
            {
                "name": "led",
                "index": 0,
                "pin": "A1",
                "direction": "out",
                "buffer": "obuf",
                "iostandard": "LVCMOS33"
            }
        ],
        "valid": True
    },
    {
        "id": "scalar-pin-valid-as-bus",
        "signal": {
            "name": "led",
            "pin": "A1",
            "bank": 34,
            "direction": "out",
            "buffer": "obuf",
            "as_bus": True
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"}
        },
        "expected": [
            {
                "name": "led",
                "index": 0,
                "pin": "A1",
                "direction": "out",
                "buffer": "obuf",
                "iostandard": "LVCMOS33"
            }
        ],
        "valid": True
    },
    {
        "id": "scalar-pin-missing-bank",
        "signal": {
            "name": "led",
            "pin": "Z99",
            "direction": "out",
            "buffer": "obuf"
        },
        "banks": {},
        "valid": False
    },
    {
        "id": "scalar-pin-explicit-iostandard",
        "signal": {
            "name": "led",
            "pin": "A2",
            "direction": "out",
            "buffer": "obuf",
            "iostandard": "LVCMOS18"
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"}
        },
        "expected": [
            {
                "name": "led",
                "index": 0,
                "pin": "A2",
                "direction": "out",
                "buffer": "obuf",
                "iostandard": "LVCMOS18"
            }
        ],
        "valid": True
    }
]

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_flatten_signal_pin_scalar(case):
    if case["valid"]:
        result = flatten_signal_pin_scalar(case["signal"], case["banks"])
        assert_flat_signals_equal(result, case["expected"])
    else:
        with pytest.raises(Exception):
            flatten_signal_pin_scalar(case["signal"], case["banks"])
