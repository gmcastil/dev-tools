import pytest
from io_gen import pin_table

BANKS = {
    34: {"iostandard": "LVCMOS33"},
    35: {"iostandard": "LVCMOS18"},
}

CASES = [
    # Bank-inherited scalar
    {
        "id": "scalar-inherit-iostandard",
        "signal": {
            "name": "led",
            "direction": "out",
            "buffer": "obuf",
            "pins": "R14",
            "bank": 34,
            "width": 1,
            "bus": False,
            "diff_pair": False,
        },
        "expected": [
            {
                "name": "led",
                "direction": "out",
                "pin": "R14",
                "buffer": "obuf",
                "bus": False,
                "iostandard": "LVCMOS33",
                "diff_pair": False,
                "index": 0,
            }
        ],
        "func": pin_table.flatten_scalar_pins,
    },
    # Bank-inherited array
    {
        "id": "array-inherit-iostandard",
        "signal": {
            "name": "sw",
            "direction": "in",
            "buffer": "ibuf",
            "pins": ["A1", "B2", "C3"],
            "bank": 35,
            "width": 3,
            "bus": True,
            "diff_pair": False,
        },
        "expected": [
            {
                "name": "sw",
                "direction": "in",
                "pin": "A1",
                "buffer": "ibuf",
                "bus": True,
                "iostandard": "LVCMOS18",
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
                "pin": "C3",
                "buffer": "ibuf",
                "bus": True,
                "iostandard": "LVCMOS18",
                "diff_pair": False,
                "index": 2,
            },
        ],
        "func": pin_table.flatten_array_pins,
    },
    # Signal-level override scalar
    {
        "id": "scalar-override-iostandard",
        "signal": {
            "name": "led_ovr",
            "direction": "out",
            "buffer": "obuf",
            "pins": "T1",
            "iostandard": "LVCMOS12",
            "width": 1,
            "bus": False,
            "diff_pair": False,
        },
        "expected": [
            {
                "name": "led_ovr",
                "direction": "out",
                "pin": "T1",
                "buffer": "obuf",
                "bus": False,
                "iostandard": "LVCMOS12",
                "diff_pair": False,
                "index": 0,
            }
        ],
        "func": pin_table.flatten_scalar_pins,
    },
    # Signal-level override array
    {
        "id": "array-override-iostandard",
        "signal": {
            "name": "btn_ovr",
            "direction": "in",
            "buffer": "ibuf",
            "pins": ["D1", "E2"],
            "iostandard": "LVCMOS25",
            "width": 2,
            "bus": True,
            "diff_pair": False,
        },
        "expected": [
            {
                "name": "btn_ovr",
                "direction": "in",
                "pin": "D1",
                "buffer": "ibuf",
                "bus": True,
                "iostandard": "LVCMOS25",
                "diff_pair": False,
                "index": 0,
            },
            {
                "name": "btn_ovr",
                "direction": "in",
                "pin": "E2",
                "buffer": "ibuf",
                "bus": True,
                "iostandard": "LVCMOS25",
                "diff_pair": False,
                "index": 1,
            },
        ],
        "func": pin_table.flatten_array_pins,
    },
]

@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_flatten_pins(case):
    result = case["func"](case["signal"], BANKS)
    assert result == case["expected"]
