import pytest

from io_gen.normalize import normalize
from io_gen.annotate import annotate

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

def test_normalize_preserves_bus_flag():
    data = {
        "title": "Bus Test",
        "part": "xc7z020",
        "banks": [{
            "bank": 34,
            "iostandard": "LVCMOS33",
            "performance": "HP"
        }],
        "signals": [{
            "name": "bus_signal",
            "direction": "out",
            "buffer": "obuf",
            "bank": 34,
            "pin": "A1",
            "bus": True
        }]
    }
    result = normalize(data)
    assert result["signals"][0]["bus"] is True

def test_normalize_preserves_group():
    data = {
        "title": "Group Test",
        "part": "xc7z020",
        "banks": [{
            "bank": 34,
            "iostandard": "LVCMOS33",
            "performance": "HP"
        }],
        "signals": [{
            "name": "grouped",
            "direction": "in",
            "buffer": "ibuf",
            "bank": 34,
            "pin": "A1",
            "group": "gpio"
        }]
    }
    result = normalize(data)
    assert result["signals"][0]["group"] == "gpio"

def test_normalize_and_annotate_pin():
    data = {
        'title': 'pin test',
        'part': 'xc7z020',
        'banks': [{
            'bank': 34,
            'iostandard': 'LVCMOS33',
            'performance': 'HP'
        }],
        'signals': [{
            'name': 's', 'direction': 'in', 'buffer': 'ibuf',
            'bank': 34, 'pin': 'A1'
        }]
    }
    result = annotate(normalize(data))
    s = result['signals'][0]
    assert s['iostandard'] == 'LVCMOS33'
    assert s['width'] == 1

def test_normalize_and_annotate_pins_bus():
    data = {
        'title': 'pins test',
        'part': 'xc7z020',
        'banks': [{
            'bank': 34,
            'iostandard': 'LVCMOS18',
            'performance': 'HR'
        }],
        'signals': [{
            'name': 'd', 'direction': 'out', 'buffer': 'obuf',
            'bank': 34, 'pins': ['A1', 'A2'], 'bus': True
        }]
    }
    result = annotate(normalize(data))
    s = result['signals'][0]
    assert s['iostandard'] == 'LVCMOS18'
    assert s['width'] == 2

def test_normalize_and_annotate_pinset_bus():
    data = {
        'title': 'pinset test',
        'part': 'xc7z020',
        'banks': [{
            'bank': 33,
            'iostandard': 'LVCMOS15',
            'performance': 'HD'
        }],
        'signals': [{
            'name': 'diff', 'direction': 'in', 'buffer': 'ibuf',
            'bank': 33, 'pinset': {
                'p': ['A1', 'A2'],
                'n': ['B1', 'B2']
            },
            'bus': True
        }]
    }
    result = annotate(normalize(data))
    s = result['signals'][0]
    assert s['iostandard'] == 'LVCMOS15'
    assert s['width'] == 2

def test_normalize_and_annotate_raises_on_mismatched_pinset():
    data = {
        'title': 'bad pinset',
        'part': 'xc7z020',
        'banks': [{
            'bank': 35,
            'iostandard': 'LVCMOS33',
            'performance': 'HP'
        }],
        'signals': [{
            'name': 'err', 'direction': 'in', 'buffer': 'ibuf',
            'bank': 35, 'pinset': {
                'p': ['A1', 'A2'],
                'n': ['B1']
            },
            'bus': True
        }]
    }
    with pytest.raises(ValueError, match='equal length'):
        annotate(normalize(data))

