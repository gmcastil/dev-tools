import pytest
from io_gen.pin_table import flatten_signal_multibank
from tests.utils import assert_flat_signals_equal

cases = [
    {
        "id": "multibank-invalid-as-bus-present",
        "signal": {
            "name": "data",
            "as_bus": True,
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
        "valid": False
    }
]

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_flatten_signal_multibank_as_bus_rejected(case):
    if case["valid"]:
        result = flatten_signal_multibank(case["signal"], case["banks"])
        assert_flat_signals_equal(result, case["expected"])
    else:
        with pytest.raises(Exception):
            flatten_signal_multibank(case["signal"], case["banks"])
