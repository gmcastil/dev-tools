"""
Unit tests for semantic validation (check phase).
Each test corresponds to a check_*() function in io_gen.check.

"""

import pytest
from io_gen.check import (
    check_duplicate_names,
    check_duplicate_pins,
    check_bus_misuse
)

# --- Duplicate name checks
def test_duplicate_names_raises():
    signals = [
        {"name": "clk", "pin": "A1"},
        {"name": "clk", "pin": "A2"},
    ]
    with pytest.raises(ValueError, match=r"(?i)duplicate signal name"):
        check_duplicate_names(signals)

def test_unique_names_pass():
    signals = [
        {"name": "clk", "pin": "A1"},
        {"name": "rst", "pin": "A2"},
    ]
    check_duplicate_names(signals)  # Should not raise

# --- Duplicate pin usage
def test_duplicate_pins_raises():
    signals = [
        {"name": "a", "pin": "A1"},
        {"name": "b", "pin": "A1"},
    ]
    with pytest.raises(ValueError, match=r"(?i)duplicate pin name"):
        check_duplicate_pins(signals)

def test_unique_pins_pass():
    signals = [
        {"name": "a", "pin": "A1"},
        {"name": "b", "pin": "A2"},
    ]
    check_duplicate_pins(signals)  # Should not raise

# --- Check bus usage
def test_bus_on_scalar_pin_ok():
    signals = [
        {"name": "scalar", "pin": "A1", "bus": True, "width": 1}
    ]
    check_bus_misuse(signals)  # Should not raise

def test_bus_on_scalar_pinset_ok():
    signals = [
        {"name": "diff", "pinset": {"p": "A1", "n": "B1"}, "bus": True, "width": 1}
    ]
    check_bus_misuse(signals)  # Should not raise

def test_bus_on_multibit_pins_ok():
    signals = [
        {"name": "data", "pins": ["A1", "A2", "A3"], "bus": True, "width": 3}
    ]
    check_bus_misuse(signals)  # Should not raise

def test_bus_on_multibit_pinset_ok():
    signals = [
        {"name": "diff_data", "pinset": {"p": ["A1", "A2"], "n": ["B1", "B2"]}, "bus": True, "width": 2}
    ]
    check_bus_misuse(signals)  # Should not raise

# --- Invalid usage of 'bus'
def test_multibit_bus_false_raises():
    signals = [
        {"name": "addr", "pins": ["A1", "A2", "A3"], "bus": False, "width": 3}
    ]
    with pytest.raises(ValueError, match="sets 'bus: false'"):
        check_bus_misuse(signals)

def test_multibit_pinset_bus_false_raises():
    signals = [
        {"name": "diff_addr", "pinset": {"p": ["A1", "A2"], "n": ["B1", "B2"]}, "bus": False, "width": 2}
    ]
    with pytest.raises(ValueError, match="sets 'bus: false'"):
        check_bus_misuse(signals)
