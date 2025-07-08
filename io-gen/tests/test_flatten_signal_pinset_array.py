import pytest
from io_gen.pin_table import flatten_signal_pinset_array
from tests.utils import assert_flat_signals_equal

cases = [
    {
        "id": "pinset-array-valid",
        "signal": {
            "name": "diff",
            "pinset": {
                "p": ["A1", "A3"],
                "n": ["A2", "A4"]
            },
            "bank": 34,
            "direction": "in",
            "buffer": "ibuf"
        },
        "banks": {
            34: {"iostandard": "LVDS"}
        },
        "expected": [
            {"name": "diff", "index": 0, "p": "A1", "n": "A2", "direction": "in", "buffer": "ibuf", "iostandard": "LVDS"},
            {"name": "diff", "index": 1, "p": "A3", "n": "A4", "direction": "in", "buffer": "ibuf", "iostandard": "LVDS"}
        ],
        "valid": True
    },
    {
        "id": "pinset-array-invalid-mismatched-lengths",
        "signal": {
            "name": "diff",
            "pinset": {
                "p": ["B1"],
                "n": ["B2", "B3"]
            },
            "bank": 34,
            "direction": "in",
            "buffer": "ibuf"
        },
        "banks": {
            34: {"iostandard": "LVDS"}
        },
        "valid": False
    }
]

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_flatten_signal_pinset_array(case):
    if case["valid"]:
        result = flatten_signal_pinset_array(case["signal"], case["banks"])
        assert_flat_signals_equal(result, case["expected"])
    else:
        with pytest.raises(Exception):
            flatten_signal_pinset_array(case["signal"], case["banks"])
