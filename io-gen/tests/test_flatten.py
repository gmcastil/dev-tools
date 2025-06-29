import pytest

from io_gen.flatten import flatten_signals
from io_gen.flatten import flatten_banks

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

def test_flatten_banks_basic():
    data = {
        "title": "Test",
        "part": "xc7z020clg400-1",
        "banks": [
            {
                "bank": 34,
                "iostandard": "LVCMOS33",
                "performance": "HR",
                "comment": "used for LEDs"
            },
            {
                "bank": 35,
                "iostandard": "LVCMOS18",
                "performance": "HP"
            }
        ],
        "signals": []  # irrelevant for this test
    }

    banks = flatten_banks(data)

    assert banks == {
        34: {
            "iostandard": "LVCMOS33",
            "performance": "HR",
            "comment": "used for LEDs"
        },
        35: {
            "iostandard": "LVCMOS18",
            "performance": "HP"
        }
    }

def test_flatten_banks_duplicate_raises():
    data = {
        "title": "Test",
        "part": "xc7z020clg400-1",
        "banks": [
            {
                "bank": 34,
                "iostandard": "LVCMOS33",
                "performance": "HR"
            },
            {
                "bank": 34,  # duplicate!
                "iostandard": "LVCMOS18",
                "performance": "HP"
            }
        ],
        "signals": []
    }

    with pytest.raises(ValueError, match="Found duplicate bank 34 entry"):
        flatten_banks(data)

def test_flatten_preserves_single_element_pinset_lists():
    data = {
        "title": "Single-bit Bus",
        "part": "xc7z020clg400-1",
        "banks": [{"bank": 34, "iostandard": "LVDS_25", "performance": "HR"}],
        "signals": [
            {
                "name": "clk_diff",
                "direction": "in",
                "buffer": "ibufds",
                "bank": 34,
                "pinset": {
                    "p": ["A12"],
                    "n": ["A11"]
                }
            }
        ]
    }

    flat = flatten_signals(data)

    assert isinstance(flat[0]["pinset"]["p"], list)
    assert flat[0]["pinset"]["p"] == ["A12"]
    assert flat[0]["pinset"]["n"] == ["A11"]

def test_flatten_preserves_width_1_pinset_bus():
    """
    Flattening should preserve the array-like nature of signals because hardware
    will eventually be inferred from this (e.g., std_logic_vector(0 downto 0) is not
    the same as std_logic)

    Flattening should not collapse ["A12"] -> "A12" just because the list has length 1.

    """
    data = {
        "title": "Single-bit Differential Bus",
        "part": "xc7z020clg400-1",
        "banks": [
            {
                "bank": 34,
                "iostandard": "LVDS_25",
                "performance": "HR"
            }
        ],
        "signals": [
            {
                "name": "diff_bus_1bit",
                "direction": "in",
                "buffer": "ibufds",
                "bank": 34,
                "pinset": {
                    "p": ["A12"],
                    "n": ["A11"]
                }
            }
        ]
    }

    flat = flatten_signals(data)
    signal = flat[0]

    assert signal["name"] == "diff_bus_1bit"
    assert isinstance(signal["pinset"]["p"], list)
    assert isinstance(signal["pinset"]["n"], list)
    assert signal["pinset"]["p"] == ["A12"]
    assert signal["pinset"]["n"] == ["A11"]

def test_flatten_preserves_single_element_pins_bus():
    """
    Flattening should preserve the array-like nature of signals because hardware
    will eventually be inferred from this (e.g., std_logic_vector(0 downto 0) is not
    the same as std_logic)

    """
    data = {
        "title": "1-bit Bus Signal",
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
                "name": "bus_out",
                "direction": "out",
                "buffer": "obuf",
                "bank": 34,
                "pins": ["A1"]
            }
        ]
    }

    flat = flatten_signals(data)
    signal = flat[0]

    assert signal["name"] == "bus_out"
    assert isinstance(signal["pins"], list)
    assert signal["pins"] == ["A1"]

