import pytest
from io_gen import pin_table

BANKS = {
    34: {"iostandard": "LVDS"},
    35: {"iostandard": "TMDS_33"},
}

CASES = [
    # Scalar differential, inherited iostandard
    {
        "id": "scalar-pinset-inherit",
        "signal": {
            "name": "clk",
            "direction": "in",
            "buffer": "ibufds",
            "pinset": {"p": "A1", "n": "A2"},
            "bank": 34,
            "width": 1,
            "bus": False,
            "diff_pair": True,
        },
        "expected": [
            {
                "name": "clk",
                "direction": "in",
                "p": "A1",
                "n": "A2",
                "buffer": "ibufds",
                "bus": False,
                "iostandard": "LVDS",
                "diff_pair": True,
                "index": 0,
            }
        ],
        "func": pin_table.flatten_scalar_pinset,
    },
    # Array differential, inherited iostandard
    {
        "id": "array-pinset-inherit",
        "signal": {
            "name": "hdmi",
            "direction": "out",
            "buffer": "obufds",
            "pinset": {
                "p": ["B1", "C1"],
                "n": ["B2", "C2"]
            },
            "bank": 35,
            "width": 2,
            "bus": True,
            "diff_pair": True,
        },
        "expected": [
            {
                "name": "hdmi",
                "direction": "out",
                "p": "B1",
                "n": "B2",
                "buffer": "obufds",
                "bus": True,
                "iostandard": "TMDS_33",
                "diff_pair": True,
                "index": 0,
            },
            {
                "name": "hdmi",
                "direction": "out",
                "p": "C1",
                "n": "C2",
                "buffer": "obufds",
                "bus": True,
                "iostandard": "TMDS_33",
                "diff_pair": True,
                "index": 1,
            },
        ],
        "func": pin_table.flatten_array_pinset,
    },
    # Scalar differential, explicit iostandard
    {
        "id": "scalar-pinset-override",
        "signal": {
            "name": "clk_ovr",
            "direction": "in",
            "buffer": "ibufds",
            "pinset": {"p": "D1", "n": "D2"},
            "iostandard": "LVDS_25",
            "width": 1,
            "bus": False,
            "diff_pair": True,
        },
        "expected": [
            {
                "name": "clk_ovr",
                "direction": "in",
                "p": "D1",
                "n": "D2",
                "buffer": "ibufds",
                "bus": False,
                "iostandard": "LVDS_25",
                "diff_pair": True,
                "index": 0,
            }
        ],
        "func": pin_table.flatten_scalar_pinset,
    },
    # Array differential, explicit iostandard
    {
        "id": "array-pinset-override",
        "signal": {
            "name": "tx_ovr",
            "direction": "out",
            "buffer": "obufds",
            "pinset": {
                "p": ["E1", "F1"],
                "n": ["E2", "F2"]
            },
            "iostandard": "TMDS_25",
            "width": 2,
            "bus": True,
            "diff_pair": True,
        },
        "expected": [
            {
                "name": "tx_ovr",
                "direction": "out",
                "p": "E1",
                "n": "E2",
                "buffer": "obufds",
                "bus": True,
                "iostandard": "TMDS_25",
                "diff_pair": True,
                "index": 0,
            },
            {
                "name": "tx_ovr",
                "direction": "out",
                "p": "F1",
                "n": "F2",
                "buffer": "obufds",
                "bus": True,
                "iostandard": "TMDS_25",
                "diff_pair": True,
                "index": 1,
            },
        ],
        "func": pin_table.flatten_array_pinset,
    },
]

@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_flatten_pinsets(case):
    result = case["func"](case["signal"], BANKS)
    assert result == case["expected"]
