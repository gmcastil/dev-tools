import pytest

from tests.fixtures.parsed_data import get_signals
from io_gen.signal_table import extract_signal_table, validate_signal_table

def test_extract_signal_table():

    # Use the accessor function from the fixtures to obtain the signals
    # list fro the golden YAML file and then extact the signal table from it
    actual = extract_signal_table(get_signals())

    expected = {
        'reset_n': {
            'width': 1,
            'group': '',
            'comment': '',
            'as_bus': True
            },
        'led0': {
            'width': 1,
            'group': '',
            'comment': '',
            'as_bus': False
            },
        'gpio': {
            'width': 4,
            'group': '',
            'comment': '',
            'as_bus': False
            },
        'clk_diff': {
            'width': 1,
            'group': '',
            'comment': '',
            'as_bus': False
            },
        'diff_data': {
            'width': 2,
            'group': '',
            'comment': '',
            'as_bus': False
            },
        'data_bus': {
            'width': 4,
            'group': '',
            'comment': '',
            'as_bus': False
            },
        'flag': {
            'width': 1,
            'group': '',
            'comment': '',
            'as_bus': False
            },
        'sync_diff': {
            'width': 2,
            'group': '',
            'comment': '',
            'as_bus': False
            }
        }

    assert actual == expected

def test_valid_signal_table_passes():
    signals = get_signals()
    signal_table = extract_signal_table(signals)
    # Should not raise
    validate_signal_table(signal_table)

def test_duplicate_signal_name_raises():
    signals = [
        {"name": "dup", "pin": "A1", "buffer": "ibuf", "direction": "in"},
        {"name": "dup", "pin": "A2", "buffer": "ibuf", "direction": "in"}
    ]
    with pytest.raises(ValueError, match=r"(i?)uplicate signal name"):
        signal_table = extract_signal_table(signals)

def test_missing_width_for_pins_raises():
    signals = [
        {"name": "no_width", "pins": ["A1", "A2"]}  # width is required
    ]
    with pytest.raises(ValueError, match=r"no_width.*width"):
        extract_signal_table(signals)  # this is enforced during extraction

def test_pinset_mismatch_types_raises():
    signals = [
        {
            "name": "bad_pinset",
            "pinset": {
                "p": "A1",
                "n": ["A2"]
            }
        }
    ]
    with pytest.raises(ValueError, match=r"bad_pinset.*mismatched types"):
        extract_signal_table(signals)

def test_multibank_missing_width_raises():
    signals = [
        {
            "name": "mb",
            "multibank": [{"bank": 34, "pin": "A1"}]
        }
    ]
    with pytest.raises(ValueError, match=r"mb.*width"):
        extract_signal_table(signals)

