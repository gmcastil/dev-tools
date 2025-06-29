import pytest

from io_gen.flatten import flatten_signals

def test_flatten_with_all_pin_types_and_group():
    data = {
        "title": "Test Project",
        "part": "xc7z020clg400-1",
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33", "performance": "HR"},
            {"bank": 35, "iostandard": "LVCMOS18", "performance": "HP"},
        ],
        "signals": [
            {
                "name": "led",
                "direction": "out",
                "buffer": "obuf",
                "group": "led",
                "bank": 34,
                "pin": "E12"
            },
            {
                "name": "btn",
                "direction": "in",
                "buffer": "ibuf",
                "group": "switch",
                "bank": 35,
                "pins": ["F13", "F14"]
            },
            {
                "name": "diff_clk",
                "direction": "in",
                "buffer": "ibufds",
                "group": "clock",
                "bank": 35,
                "pinset": {"p": "G15", "n": "H15"}
            },
            {
                "name": "diff_data",
                "direction": "out",
                "buffer": "obufds",
                "group": "uart",
                "bank": 34,
                "pinset": {
                    "p": ["J16", "K16"],
                    "n": ["J15", "K15"]
                }
            }
        ]
    }

    flat = flatten_signals(data)

    assert flat == [
        {
            "name": "led",
            "direction": "out",
            "buffer": "obuf",
            "group": "led",
            "bank": 34,
            "pin": "E12",
            "iostandard": "LVCMOS33"
        },
        {
            "name": "btn",
            "direction": "in",
            "buffer": "ibuf",
            "group": "switch",
            "bank": 35,
            "pins": ["F13", "F14"],
            "iostandard": "LVCMOS18"
        },
        {
            "name": "diff_clk",
            "direction": "in",
            "buffer": "ibufds",
            "group": "clock",
            "bank": 35,
            "pinset": {"p": "G15", "n": "H15"},
            "iostandard": "LVCMOS18"
        },
        {
            "name": "diff_data",
            "direction": "out",
            "buffer": "obufds",
            "group": "uart",
            "bank": 34,
            "pinset": {
                "p": ["J16", "K16"],
                "n": ["J15", "K15"]
            },
            "iostandard": "LVCMOS33"
        }
    ]

def test_flatten_inherits_iostandard():
    data = {
        "title": "IO Inheritance",
        "part": "xc7z020clg400-1",
        "banks": [
            {
                "bank": 34,
                "iostandard": "LVCMOS33",
                "performance": "HR"
            }
        ],
        "signals": [
            {
                "name": "led",
                "direction": "out",
                "buffer": "obuf",
                "bank": 34,
                "pin": "E12"
                # no iostandard given
            }
        ]
    }

    flat = flatten_signals(data)

    assert flat == [
        {
            "name": "led",
            "direction": "out",
            "buffer": "obuf",
            "bank": 34,
            "pin": "E12",
            "iostandard": "LVCMOS33"  # inherited from bank
        }
    ]

def test_flatten_iostandard_override():
    data = {
        "title": "IO Override",
        "part": "xc7z020clg400-1",
        "banks": [
            {
                "bank": 35,
                "iostandard": "LVCMOS18",
                "performance": "HP"
            }
        ],
        "signals": [
            {
                "name": "clk",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 35,
                "pin": "G15",
                "iostandard": "LVDS_25"  # overrides the bank
            }
        ]
    }

    flat = flatten_signals(data)

    assert flat == [
        {
            "name": "clk",
            "direction": "in",
            "buffer": "ibuf",
            "bank": 35,
            "pin": "G15",
            "iostandard": "LVDS_25"  # override wins
        }
    ]

