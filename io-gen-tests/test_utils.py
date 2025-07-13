import pytest
from io_gen.utils import (
    is_pins_scalar,
    is_pins_array,
    is_pinset_scalar,
    is_pinset_array,
    is_multibank
)

def test_is_pins_scalar():
    assert is_pins_scalar({"pins": "A1"})
    assert not is_pins_scalar({"pins": ["A1", "A2"]})
    assert not is_pins_scalar({"pinset": {"p": "A1", "n": "A2"}})
    assert not is_pins_scalar({"pinset": {"p": ["A1", "B1"], "n": ["A2", "B2"]}})

def test_is_pins_array():
    assert is_pins_array({"pins": ["A1", "A2"]})
    assert not is_pins_array({"pins": "A1"})
    assert not is_pins_array({"pinset": {"p": "A1", "n": "A2"}})

def test_is_pinset_scalar():
    assert is_pinset_scalar({"name": "clk", "pinset": {"p": "P1", "n": "N1"}})
    assert not is_pinset_scalar({"name": "data", "pinset": {"p": ["P1", "P2"], "n": ["N1", "N2"]}})
    assert not is_pinset_scalar({"pins": "A1"})

def test_is_pinset_array():
    assert is_pinset_array({"name": "diff_bus", "pinset": {"p": ["P1", "P2"], "n": ["N1", "N2"]}})
    assert not is_pinset_array({"name": "clk", "pinset": {"p": "P1", "n": "N1"}})
    assert not is_pinset_array({"pins": "A1"})

def test_is_multibank():
    assert is_multibank({"multibank": [{"bank": 34, "pins": "A1"}]})
    assert is_multibank({"multibank": [{"bank": 35, "pinset": {"p": "P1", "n": "N1"}}]})
    assert not is_multibank({"pins": "A1"})
    assert not is_multibank({"pinset": {"p": "P1", "n": "N1"}})

def test_pinset_type_mismatch_raises_scalar():
    with pytest.raises(ValueError, match="mismatched types"):
        is_pinset_scalar({
            "name": "bad_diff",
            "pinset": {"p": "A1", "n": ["A2"]}
        })

def test_pinset_type_mismatch_raises_array():
    with pytest.raises(ValueError, match="mismatched types"):
        is_pinset_array({
            "name": "bad_diff",
            "pinset": {"p": ["A1"], "n": "A2"}
        })

def test_pinset_unsupported_type_raises():
    with pytest.raises(ValueError, match="unsupported pinset types"):
        is_pinset_scalar({
            "name": "bad_diff",
            "pinset": {"p": 42, "n": 42}
        })

    with pytest.raises(ValueError, match="unsupported pinset types"):
        is_pinset_array({
            "name": "bad_diff",
            "pinset": {"p": 42, "n": 42}
        })

