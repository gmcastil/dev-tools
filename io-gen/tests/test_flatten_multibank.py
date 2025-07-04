import pytest
from copy import deepcopy
from io_gen.flatten import flatten_multibank

test_cases = [
    {
        "id": "valid_split_single_then_rest",
        "valid": True,
        "signal": {
            "name": "data_bus",
            "direction": "out",
            "buffer": "obuf",
            "width": 5,
            "multibank": [
                {
                    "bank": 34,
                    "offset": 0,
                    "pin": "A1"
                },
                {
                    "bank": 35,
                    "offset": 1,
                    "pins": ["B1", "B2", "B3", "B4"]
                }
            ]
        },
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33"},
            {"bank": 35, "iostandard": "LVCMOS18"}
        ],
        "expected": [
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 34, "iostandard": "LVCMOS33", "pin": "A1", "index": 0},
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 35, "iostandard": "LVCMOS18", "pin": "B1", "index": 1},
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 35, "iostandard": "LVCMOS18", "pin": "B2", "index": 2},
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 35, "iostandard": "LVCMOS18", "pin": "B3", "index": 3},
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 35, "iostandard": "LVCMOS18", "pin": "B4", "index": 4}
        ]
    },
    {
        "id": "valid_multibank_single_pin",
        "valid": True,
        "signal": {
            "name": "control",
            "direction": "in",
            "buffer": "ibuf",
            "width": 1,
            "multibank": [
                {
                    "bank": 34,
                    "offset": 0,
                    "pin": "A9"
                }
            ]
        },
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33"}
        ],
        "expected": [
            {"name": "control", "direction": "in", "buffer": "ibuf", "bank": 34, "iostandard": "LVCMOS33", "pin": "A9", "index": 0}
        ]
    },
    {
        "id": "valid_multibank_single_bit_bus",
        "valid": True,
        "signal": {
            "name": "flag",
            "direction": "in",
            "buffer": "ibuf",
            "width": 1,
            "bus": True,
            "multibank": [
                {
                    "bank": 34,
                    "offset": 0,
                    "pin": "A1"
                }
            ]
        },
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33"}
        ],
        "expected": [
            {
                "name": "flag",
                "direction": "in",
                "buffer": "ibuf",
                "bus": True,
                "index": 0,
                "bank": 34,
                "iostandard": "LVCMOS33",
                "pin": "A1"
            }
        ]
    },
    {
        "id": "valid_split_diffpair_across_two_banks",
        "valid": True,
        "signal": {
            "name": "diff_signal",
            "direction": "in",
            "buffer": "ibufds",
            "width": 3,
            "multibank": [
                {
                    "bank": 34,
                    "offset": 0,
                    "pinset": {
                        "p": "A1",
                        "n": "B1"
                    }
                },
                {
                    "bank": 35,
                    "offset": 1,
                    "pinset": {
                        "p": ["A2", "A3"],
                        "n": ["B2", "B3"]
                    }
                }
            ]
        },
        "banks": [
            {"bank": 34, "iostandard": "LVDS_25"},
            {"bank": 35, "iostandard": "LVDS_25"}
        ],
        "expected": [
            {"name": "diff_signal", "direction": "in", "buffer": "ibufds", "bank": 34, "iostandard": "LVDS_25", "p": "A1", "n": "B1", "index": 0},
            {"name": "diff_signal", "direction": "in", "buffer": "ibufds", "bank": 35, "iostandard": "LVDS_25", "p": "A2", "n": "B2", "index": 1},
            {"name": "diff_signal", "direction": "in", "buffer": "ibufds", "bank": 35, "iostandard": "LVDS_25", "p": "A3", "n": "B3", "index": 2}
        ]
    }
]

@pytest.mark.parametrize("case", test_cases, ids=[c["id"] for c in test_cases])
def test_flatten_multibank(case):
    signal = deepcopy(case["signal"])
    banks = {b["bank"]: b for b in case["banks"]}

    if case["valid"]:
        result = flatten_multibank(signal, banks)
        assert result == case["expected"]
    else:
        with pytest.raises(ValueError):
            flatten_multibank(signal, banks)
