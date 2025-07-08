import pytest
from io_gen.pin_table import flatten_signal_pinset_scalar
from tests.utils import assert_flat_signals_equal

cases = [
    {
        "id": "pinset-scalar-valid",
        "signal": {
            "name": "clk",
            "pinset": {"p": "A1", "n": "A2"},
            "bank": 34,
            "direction": "in",
            "buffer": "ibuf"
        },
        "banks": {
            34: {"iostandard": "LVDS"}
        },
        "expected": [
            {
                "name": "clk",
                "index": 0,
                "p": "A1",
                "n": "A2",
                "direction": "in",
                "buffer": "ibuf",
                "iostandard": "LVDS"
            }
        ],
        "valid": True
    },
    {
        "id": "pinset-scalar-explicit-iostandard",
        "signal": {
            "name": "clk",
            "pinset": {"p": "B1", "n": "B2"},
            "bank": 34,
            "direction": "in",
            "buffer": "ibuf",
            "iostandard": "LVDS_25"
        },
        "banks": {
            34: {"iostandard": "LVDS"}
        },
        "expected": [
            {
                "name": "clk",
                "index": 0,
                "p": "B1",
                "n": "B2",
                "direction": "in",
                "buffer": "ibuf",
                "iostandard": "LVDS_25"
            }
        ],
        "valid": True
    },
    {
        "id": "pinset-scalar-invalid-missing-n",
        "signal": {
            "name": "clk",
            "pinset": {"p": "C1"},
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
def test_flatten_signal_pinset_scalar(case):
    if case["valid"]:
        result = flatten_signal_pinset_scalar(case["signal"], case["banks"])
        assert_flat_signals_equal(result, case["expected"])
    else:
        with pytest.raises(Exception):
            flatten_signal_pinset_scalar(case["signal"], case["banks"])
