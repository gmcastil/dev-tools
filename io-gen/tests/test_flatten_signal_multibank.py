import pytest
from io_gen.pin_table import flatten_signal_multibank
from tests.utils import assert_flat_signals_equal

cases = [
    {
        "id": "multibank-array-pins-valid",
        "signal": {
            "name": "data",
            "multibank": [
                {"bank": 34, "pins": ["A1", "A2"]},
                {"bank": 35, "pins": ["B1", "B2"]}
            ],
            "direction": "in",
            "buffer": "ibuf"
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"},
            35: {"iostandard": "LVCMOS33"}
        },
        "expected": [
            {"name": "data", "index": 0, "pin": "A1", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS33"},
            {"name": "data", "index": 1, "pin": "A2", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS33"},
            {"name": "data", "index": 2, "pin": "B1", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS33"},
            {"name": "data", "index": 3, "pin": "B2", "direction": "in", "buffer": "ibuf", "iostandard": "LVCMOS33"}
        ],
        "valid": True
    },
    {
        "id": "multibank-mixed-types-invalid",
        "signal": {
            "name": "mixed",
            "multibank": [
                {"bank": 34, "pins": ["A1", "A2"]},
                {"bank": 35, "pinset": {"p": "B1", "n": "B2"}}
            ],
            "direction": "out",
            "buffer": "obuf"
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"},
            35: {"iostandard": "LVDS"}
        },
        "valid": False
    }
]

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_flatten_signal_multibank(case):
    if case["valid"]:
        result = flatten_signal_multibank(case["signal"], case["banks"])
        assert_flat_signals_equal(result, case["expected"])
    else:
        with pytest.raises(Exception):
            flatten_signal_multibank(case["signal"], case["banks"])
