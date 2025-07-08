import pytest
from io_gen.utils import (
    is_pin,
    is_pins,
    is_pinset_scalar,
    is_pinset_array,
    is_multibank
)

def test_is_pin():
    assert is_pin({"pin": "A1"})
    assert not is_pin({"pin": ["A1", "A2"]})
    assert not is_pin({"pins": ["A1", "A2"]})
    assert not is_pin({"pinset": {"p": "A1", "n": "A2"}})

def test_is_pins():
    assert is_pins({"pins": ["A1", "A2"]})
    assert not is_pins({"pin": "A1"})
    assert not is_pins({"pinset": {"p": "A1", "n": "A2"}})

def test_is_pinset_scalar():
    assert is_pinset_scalar({"name": "clk", "pinset": {"p": "P1", "n": "N1"}})
    assert not is_pinset_scalar({"name": "data", "pinset": {"p": ["P1", "P2"], "n": ["N1", "N2"]}})
    assert not is_pinset_scalar({"pin": "A1"})

def test_is_pinset_array():
    assert is_pinset_array({"name": "diff_bus", "pinset": {"p": ["P1", "P2"], "n": ["N1", "N2"]}})
    assert not is_pinset_array({"name": "clk", "pinset": {"p": "P1", "n": "N1"}})
    assert not is_pinset_array({"pin": "A1"})

def test_is_multibank():
    assert is_multibank({"multibank": [{"bank": 34, "pin": "A1"}]})
    assert is_multibank({"multibank": [{"bank": 35, "pinset": {"p": "P1", "n": "N1"}}]})
    assert not is_multibank({"pin": "A1"})
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

