import pytest

from io_gen import pin_table

BANKS = {
    34: {"iostandard": "LVCMOS33"},
    35: {"iostandard": "LVCMOS18"},
}

CASES = [
    # One fragment, one pin
    {
        "id": "single-fragment-scalar-pin",
        "signal": {
            "name": "led",
            "direction": "out",
            "buffer": "obuf",
            "multibank": [{"pins": "A1", "bank": 34, "offset": 0}],
            "width": 1,
            "bus": False,
            "diff_pair": False,
        },
        "expected": [
            {
                "name": "led",
                "direction": "out",
                "pin": "A1",
                "buffer": "obuf",
                "bus": False,
                "iostandard": "LVCMOS33",
                "diff_pair": False,
                "index": 0,
            }
        ],
        "func": pin_table.flatten_multibank_pins,
    },
    # Multiple fragments, each with one pin
    {
        "id": "multiple-fragments-mixed-banks",
        "signal": {
            "name": "sw",
            "direction": "in",
            "buffer": "ibuf",
            "multibank": [
                {"pins": "B1", "bank": 34, "offset": 0},
                {"pins": "B2", "bank": 35, "offset": 1},
                {"pins": "B3", "bank": 34, "offset": 2},
            ],
            "width": 3,
            "bus": True,
            "diff_pair": False,
        },
        "expected": [
            {
                "name": "sw",
                "direction": "in",
                "pin": "B1",
                "buffer": "ibuf",
                "bus": True,
                "iostandard": "LVCMOS33",
                "diff_pair": False,
                "index": 0,
            },
            {
                "name": "sw",
                "direction": "in",
                "pin": "B2",
                "buffer": "ibuf",
                "bus": True,
                "iostandard": "LVCMOS18",
                "diff_pair": False,
                "index": 1,
            },
            {
                "name": "sw",
                "direction": "in",
                "pin": "B3",
                "buffer": "ibuf",
                "bus": True,
                "iostandard": "LVCMOS33",
                "diff_pair": False,
                "index": 2,
            },
        ],
        "func": pin_table.flatten_multibank_pins,
    },
    # One fragment with pins array
    {
        "id": "single-fragment-multiple-pins",
        "signal": {
            "name": "gpio",
            "direction": "inout",
            "buffer": "iobuf",
            "multibank": [{"pins": ["C1", "C2"], "bank": 35, "offset": 0}],
            "width": 2,
            "bus": True,
            "diff_pair": False,
        },
        "expected": [
            {
                "name": "gpio",
                "direction": "inout",
                "pin": "C1",
                "buffer": "iobuf",
                "bus": True,
                "iostandard": "LVCMOS18",
                "diff_pair": False,
                "index": 0,
            },
            {
                "name": "gpio",
                "direction": "inout",
                "pin": "C2",
                "buffer": "iobuf",
                "bus": True,
                "iostandard": "LVCMOS18",
                "diff_pair": False,
                "index": 1,
            },
        ],
        "func": pin_table.flatten_multibank_pins,
    },
    # Multiple fragments, with one overriding iostandard
    {
        "id": "explicit-iostandard-fragment",
        "signal": {
            "name": "btn",
            "direction": "in",
            "buffer": "ibuf",
            "iostandard": "LVCMOS12",
            "multibank": [
                {"pins": "D1", "bank": 35, "offset": 0},
                {"pins": "D2", "bank": 34, "offset": 1},
            ],
            "width": 2,
            "bus": True,
            "diff_pair": False,
        },
        "expected": [
            {
                "name": "btn",
                "direction": "in",
                "pin": "D1",
                "buffer": "ibuf",
                "bus": True,
                "iostandard": "LVCMOS12",
                "diff_pair": False,
                "index": 0,
            },
            {
                "name": "btn",
                "direction": "in",
                "pin": "D2",
                "buffer": "ibuf",
                "bus": True,
                "iostandard": "LVCMOS33",
                "diff_pair": False,
                "index": 1,
            },
        ],
        "func": pin_table.flatten_multibank_pins,
    },
]


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_flatten_multibank_pins(case):
    result = case["func"](case["signal"], BANKS)
    assert result == case["expected"]
