"""
Tests signal and bank flattening prior to annotation

"""

import pytest

from io_gen.flatten import flatten_signals
from io_gen.flatten import flatten_banks

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

    flat_banks = flatten_banks(data["banks"])

    assert flat_banks == {
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
        flatten_banks(data["banks"])

def test_flatten_with_all_pin_types_and_group():
    data = {
        "title": "Test Project",
        "part": "xc7z020clg400-1",
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33", "performance": "HR", "comment": "testing"},
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

    flat_banks = flatten_banks(data["banks"])
    flat_signals = flatten_signals(data["signals"], flat_banks)

    assert flat_signals == [
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

    flat_banks = flatten_banks(data["banks"])
    flat_signals = flatten_signals(data["signals"], flat_banks)

    assert flat_signals == [
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

    flat_banks = flatten_banks(data["banks"])
    flat_signals = flatten_signals(data["signals"], flat_banks)

    assert flat_signals == [
        {
            "name": "clk",
            "direction": "in",
            "buffer": "ibuf",
            "bank": 35,
            "pin": "G15",
            "iostandard": "LVDS_25"  # override wins
        }
    ]

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

    flat_banks = flatten_banks(data["banks"])
    flat_signals = flatten_signals(data["signals"], flat_banks)

    assert isinstance(flat_signals[0]["pinset"]["p"], list)
    assert flat_signals[0]["pinset"]["p"] == ["A12"]
    assert flat_signals[0]["pinset"]["n"] == ["A11"]

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

    flat_banks = flatten_banks(data["banks"])
    flat_signals = flatten_signals(data["signals"], flat_banks)

    signal = flat_signals[0]

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

    flat_banks = flatten_banks(data["banks"])
    flat_signals = flatten_signals(data["signals"], flat_banks)
    signal = flat_signals[0]

    assert signal["name"] == "bus_out"
    assert isinstance(signal["pins"], list)
    assert signal["pins"] == ["A1"]

def test_flatten_signals_missing_bank_raises():
    data = {
        "banks": [
            # no bank 99 defined here
            {"bank": 34, "iostandard": "LVCMOS33", "performance": "HR"}
        ],
        "signals": [
            {
                "name": "debug",
                "direction": "out",
                "buffer": "obuf",
                "bank": 99,  # not defined
                "pin": "F3"  # no iostandard specified
            }
        ]
    }

    flat_banks = flatten_banks(data["banks"])

    with pytest.raises(ValueError, match=r"Signal 'debug' refers to undefined bank 99"):
        flatten_signals(data["signals"], flat_banks)

def test_flatten_signals_does_not_mutate_input():
    original_signals = [{
        "name": "data",
        "direction": "in",
        "buffer": "ibuf",
        "bank": 34,
        "pinset": {
            "p": ["A1", "A2"],
            "n": ["B1", "B2"]
        }
    }]
    banks = {
        34: {"iostandard": "LVCMOS33", "performance": "HP"}
    }

    import copy
    signals_copy = copy.deepcopy(original_signals)
    result = flatten_signals(signals_copy, banks)

    assert signals_copy == original_signals
    assert "iostandard" not in signals_copy[0]

    assert result[0]["iostandard"] == "LVCMOS33"

