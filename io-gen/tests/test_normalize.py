import pytest

from io_gen.normalize import normalize

def test_normalize_minimal_case():
    data = {
        "title": "Test IO",
        "part": "xc7a100t",
        "banks": [{
            "bank": 34,
            "iostandard": "LVCMOS33",
            "performance": "HP"
        }],
        "signals": [{
            "name": "led",
            "direction": "out",
            "buffer": "obuf",
            "bank": 34,
            "pin": "E1"
        }]
    }

    result = normalize(data)

    assert result["banks"][34]["iostandard"] == "LVCMOS33"
    assert result["signals"][0]["iostandard"] == "LVCMOS33"

def test_normalize_signal_override():
    data = {
        "title": "Override Test",
        "part": "xc7a100t",
        "banks": [{
            "bank": 34,
            "iostandard": "LVCMOS33",
            "performance": "HP"
        }],
        "signals": [{
            "name": "led",
            "direction": "out",
            "buffer": "obuf",
            "bank": 34,
            "pin": "E1",
            "iostandard": "LVTTL"
        }]
    }

    result = normalize(data)

    assert result["signals"][0]["iostandard"] == "LVTTL"

def test_normalize_missing_inheritance_raises():
    data = {
        "title": "Bad Signal",
        "part": "xc7a100t",
        "banks": [],
        "signals": [{
            "name": "led",
            "bank": 34,
            "direction": "out",
            "buffer": "obuf",
            "pin": "E1"
        }]
    }

    with pytest.raises(ValueError):
        normalize(data)

def test_normalize_does_not_mutate_input():
    import copy
    data = {
        "title": "Immutability Test",
        "part": "xc7a100t",
        "banks": [{
            "bank": 34,
            "iostandard": "LVCMOS33",
            "performance": "HP"
        }],
        "signals": [{
            "name": "led",
            "direction": "out",
            "buffer": "obuf",
            "bank": 34,
            "pin": "E1"
        }]
    }
    original = copy.deepcopy(data)
    normalize(data)
    assert data == original

