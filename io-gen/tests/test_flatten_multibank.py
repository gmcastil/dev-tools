import pytest
from copy import deepcopy

from io_gen.flatten import flatten_multibank
from tests.utils import assert_flat_signals_equal

multibank_test_cases = [
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
        "banks": {
            34: {"iostandard": "LVCMOS33"},
            35: {"iostandard": "LVCMOS18"}
        },
        "expected": [
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 34, "iostandard": "LVCMOS33", "pin": "A1", "index": 0, "bus": False},
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 35, "iostandard": "LVCMOS18", "pin": "B1", "index": 1, "bus": False},
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 35, "iostandard": "LVCMOS18", "pin": "B2", "index": 2, "bus": False},
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 35, "iostandard": "LVCMOS18", "pin": "B3", "index": 3, "bus": False},
            {"name": "data_bus", "direction": "out", "buffer": "obuf", "bank": 35, "iostandard": "LVCMOS18", "pin": "B4", "index": 4, "bus": False}
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
        "banks": {
            34: {"iostandard": "LVCMOS33"}
        },
        "expected": [
            {"name": "control", "direction": "in", "buffer": "ibuf", "bank": 34, "iostandard": "LVCMOS33", "pin": "A9", "index": 0, "bus": False}
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
        "banks": {
            34: {"iostandard": "LVCMOS33"}
        },
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
        "id": "valid_multibank_mixed_iostandard_inheritance",
        "valid": True,
        "signal": {
            "name": "ctrl",
            "direction": "out",
            "buffer": "obuf",
            "width": 4,
            "multibank": [
                {
                    "bank": 34,
                    "offset": 0,
                    "pins": ["A1", "A2"]
                },
                {
                    "bank": 35,
                    "offset": 2,
                    "pins": ["B1", "B2"]
                }
            ]
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"},
            35: {"iostandard": "LVCMOS18"}
        },
        "expected": [
            {
                "name": "ctrl",
                "direction": "out",
                "buffer": "obuf",
                "bank": 34,
                "index": 0,
                "pin": "A1",
                "bus": False,
                "iostandard": "LVCMOS33"
            },
            {
                "name": "ctrl",
                "direction": "out",
                "buffer": "obuf",
                "bank": 34,
                "index": 1,
                "pin": "A2",
                "bus": False,
                "iostandard": "LVCMOS33"
            },
            {
                "name": "ctrl",
                "direction": "out",
                "buffer": "obuf",
                "bank": 35,
                "index": 2,
                "pin": "B1",
                "bus": False,
                "iostandard": "LVCMOS18"
            },
            {
                "name": "ctrl",
                "direction": "out",
                "buffer": "obuf",
                "bank": 35,
                "index": 3,
                "pin": "B2",
                "bus": False,
                "iostandard": "LVCMOS18"
            }
        ]
    },
    {
        "id": "reversed_offsets",
        "valid": True,
        "signal": {
            "name": "bad_signal5",
            "direction": "in",
            "buffer": "ibuf",
            "width": 4,
            "multibank": [
                {
                    "bank": 35,
                    "offset": 2,
                    "pins": ["B1", "B2"]
                },
                {
                    "bank": 34,
                    "offset": 0,
                    "pins": ["A1", "A2"]
                }
            ]
        },
        "banks": {
            34: {"iostandard": "LVCMOS33"},
            35: {"iostandard": "LVCMOS33"}
        },
        "expected": [
            {
                "name": "bad_signal5",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 34,
                "iostandard": "LVCMOS33",
                "pin": "A1",
                "bus": False,
                "index": 0
                },
            {
                "name": "bad_signal5",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 34,
                "iostandard": "LVCMOS33",
                "pin": "A2",
                "bus": False,
                "index": 1
                },
            {
                "name": "bad_signal5",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 35,
                "iostandard": "LVCMOS33",
                "pin": "B1",
                "bus": False,
                "index": 2
                },
            {
                "name": "bad_signal5",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 35,
                "iostandard": "LVCMOS33",
                "pin": "B2",
                "bus": False,
                "index": 3
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
        "banks": {
            34: {"iostandard": "LVDS_25"},
            35: {"iostandard": "LVDS_25"}
        },
        "expected": [
            {"name": "diff_signal", "direction": "in", "buffer": "ibufds", "bank": 34, "iostandard": "LVDS_25", "p": "A1", "n": "B1", "index": 0, "bus": False},
            {"name": "diff_signal", "direction": "in", "buffer": "ibufds", "bank": 35, "iostandard": "LVDS_25", "p": "A2", "n": "B2", "index": 1, "bus": False},
            {"name": "diff_signal", "direction": "in", "buffer": "ibufds", "bank": 35, "iostandard": "LVDS_25", "p": "A3", "n": "B3", "index": 2, "bus": False}
        ]
    }
]

test_ids = [c["id"] for c in multibank_test_cases]

@pytest.mark.parametrize("case", multibank_test_cases, ids=test_ids)
def test_flatten_multibank(case):
    signal = deepcopy(case["signal"])
    banks = case['banks']

    if case["valid"]:
        result = flatten_multibank(signal, banks)
        assert_flat_signals_equal(result, case['expected'])
    else:
        with pytest.raises(ValueError):
            flatten_multibank(signal, banks)
