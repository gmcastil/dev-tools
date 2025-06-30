import pytest

from io_gen.check import check

def test_duplicate_signal_names_raises():
    normalized = {
        "title": "Dup Test",
        "part": "xc7z020",
        "banks": {
            34: {
                "iostandard": "LVCMOS33",
                "performance": "HR"
            }
        },
        "signals": [
            {
                "name": "led",
                "direction": "out",
                "buffer": "obuf",
                "bank": 34,
                "pin": "A1",
                "iostandard": "LVCMOS33"
            },
            {
                "name": "led",
                "direction": "out",
                "buffer": "obuf",
                "bank": 34,
                "pin": "A2",
                "iostandard": "LVCMOS33"
            }
        ]
    }

    with pytest.raises(ValueError, match="Duplicate signal name: 'led'"):
        check(normalized)

def test_duplicate_pins_across_signals_raises():
    normalized = {
        "title": "Conflict Pins",
        "part": "xc7z020",
        "banks": {
            34: {
                "iostandard": "LVCMOS33",
                "performance": "HR"
            }
        },
        "signals": [
            {
                "name": "sig1",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 34,
                "pin": "A1",
                "iostandard": "LVCMOS33"
            },
            {
                "name": "sig2",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 34,
                "pin": "A1",
                "iostandard": "LVCMOS33"
            }
        ]
    }

    with pytest.raises(ValueError, match=r"Pins .* already claimed"):
        check(normalized)


def test_duplicate_pins_across_pins_array_raises():
    normalized = {
        "title": "Conflict Pins Array",
        "part": "xc7z020",
        "banks": {
            34: {
                "iostandard": "LVCMOS33",
                "performance": "HR"
            }
        },
        "signals": [
            {
                "name": "sig1",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 34,
                "pins": ["A1", "A2"],
                "iostandard": "LVCMOS33"
            },
            {
                "name": "sig2",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 34,
                "pins": ["A2", "A3"],
                "iostandard": "LVCMOS33"
            }
        ]
    }

    with pytest.raises(ValueError, match=r"Pins .* already claimed"):
        check(normalized)


def test_mismatched_pinset_arrays_raises():
    normalized = {
        "title": "Mismatched Pinset",
        "part": "xc7z020",
        "banks": {
            34: {
                "iostandard": "LVCMOS33",
                "performance": "HR"
            }
        },
        "signals": [
            {
                "name": "diff_pair",
                "direction": "in",
                "buffer": "ibufds",
                "bank": 34,
                "pinset": {
                    "p": ["A1", "A2"],
                    "n": ["B1"]
                },
                "iostandard": "LVCMOS33"
            }
        ]
    }

    with pytest.raises(ValueError, match="Mismatched pinset width"):
        check(normalized)


def test_valid_pinset_passes():
    normalized = {
        "title": "Good Pinset",
        "part": "xc7z020",
        "banks": {
            34: {
                "iostandard": "LVCMOS33",
                "performance": "HR"
            }
        },
        "signals": [
            {
                "name": "clk",
                "direction": "in",
                "buffer": "ibufds",
                "bank": 34,
                "pinset": {
                    "p": ["A1", "A2"],
                    "n": ["B1", "B2"]
                },
                "iostandard": "LVCMOS33"
            }
        ]
    }

    check(normalized)  # Should not raise

