import pytest
from io_gen.pin_table import flatten_signal_pins_array

from tests.utils import assert_flat_signals_equal

cases = [
    {
        "id": "pins-array-valid",
        "signal": {
            "name": "data",
            "pins": ["A1", "A2", "A3"],
            "bank": 34,
            "direction": "in",
            "buffer": "ibuf"
        },
        "banks": {
            34: {"iostandard": "LVCMOS18"}
        },
        "expected": [
            {"name": "data", "index": 0, "pin": "A1", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS18"},
            {"name": "data", "index": 1, "pin": "A2", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS18"},
            {"name": "data", "index": 2, "pin": "A3", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS18"}
        ],
        "valid": True
    },
    {
        "id": "pins-array-valid-no-bank",
        "signal": {
            "name": "data",
            "pins": ["A1", "A2", "A3"],
            "bank": 34,
            "direction": "in",
            "buffer": "ibuf",
            "iostandard": "LVCMOS18"
        },
        "banks": {
        },
        "expected": [
            {"name": "data", "index": 0, "pin": "A1", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS18"},
            {"name": "data", "index": 1, "pin": "A2", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS18"},
            {"name": "data", "index": 2, "pin": "A3", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS18"}
        ],
        "valid": True
    },
    {
        "id": "pins-array-explicit-iostandard",
        "signal": {
            "name": "data",
            "pins": ["A4", "A5"],
            "bank": 34,
            "direction": "in",
            "buffer": "ibuf",
            "iostandard": "LVCMOS25"
        },
        "banks": {
            34: {"iostandard": "LVCMOS18"}
        },
        "expected": [
            {"name": "data", "index": 0, "pin": "A4", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS25"},
            {"name": "data", "index": 1, "pin": "A5", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS25"}
        ],
        "valid": True
    }

]

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_flatten_signal_pins_array(case):
    if case["valid"]:
        result = flatten_signal_pins_array(case["signal"], case["banks"])
        assert_flat_signals_equal(result, case["expected"])
    else:
        with pytest.raises(Exception):
            flatten_signal_pins_array(case["signal"], case["banks"])
