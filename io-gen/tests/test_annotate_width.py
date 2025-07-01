"""
Unit tests for annotate_width(), which computes signal width based only on
structural pin, pins, or pinset fields. This function does not consider
the 'bus' flag or validate semantic intent.

"""
import pytest

from io_gen.annotate import annotate_width

# Tests for annotate_width() which adds the width property based on the
# presence of pin, pins, or pinsets and the bus boolean.
def test_annotate_pin_scalar():
    signal = {'pin': 'A1'}
    result = annotate_width(signal.copy())
    assert result['width'] == 1

def test_annotate_pin_bus_true():
    signal = {'pin': 'A1', 'bus': True}
    result = annotate_width(signal.copy())
    assert result['width'] == 1

def test_annotate_pins_vector():
    signal = {'pins': ['A1', 'A2']}
    result = annotate_width(signal.copy())
    assert result['width'] == 2

def test_annotate_pinset_scalar():
    signal = {'pinset': {'p': 'A1', 'n': 'B1'}}
    result = annotate_width(signal.copy())
    assert result['width'] == 1

def test_annotate_pinset_vector():
    signal = {'pinset': {'p': ['A1', 'A2'], 'n': ['B1', 'B2']}}
    result = annotate_width(signal.copy())
    assert result['width'] == 2

def test_annotate_pinset_mismatched_types_raises():
    signal = {'name': 'mismatched_types', 'pinset': {'p': ['A1'], 'n': 'B1'}}
    with pytest.raises(ValueError, match='mismatched pinset types'):
        annotate_width(signal.copy())

def test_annotate_pinset_mismatched_width_raises():
    signal = {'name': 'mismatched_widths', 'pinset': {'p': ['A1', 'A2'], 'n': ['B1']}}
    with pytest.raises(ValueError, match='must be equal lengths'):
        annotate_width(signal.copy())

def test_annotate_does_not_mutate_input():
    import copy
    from io_gen.annotate import annotate

    original = {
        "title": "Immutability Check",
        "part": "xc7z020",
        "banks": {
            34: {"iostandard": "LVCMOS33", "performance": "HR"}
        },
        "signals": [{
            "name": "sig",
            "direction": "in",
            "buffer": "ibuf",
            "bank": 34,
            "pin": "A1"
        }]
    }

    original_copy = copy.deepcopy(original)
    annotated = annotate(original_copy)

    # Ensure original wasn't changed
    assert original_copy == original
    # Ensure annotation did occur in returned object
    assert "width" in annotated["signals"][0]
    assert "width" not in original_copy["signals"][0]

