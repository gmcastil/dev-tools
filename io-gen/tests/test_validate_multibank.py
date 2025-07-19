import pytest

from io_gen.validate_signals import validate_multibank_pins, validate_multibank_pinset

cases = [
    {
        "id": "valid_multibank_pins",
        "signal": {
            "name": "data_bus",
            "multibank": [
                {"bank": 34, "pins": ["P1", "P2"], "offset": 0},
                {"bank": 35, "pins": ["P3", "P4"], "offset": 2},
            ],
            "diff_pair": False,
            "bus": True,
            "direction": "out",
            "buffer": "obuf",
            "width": 4,
        },
        "validator": validate_multibank_pins,
        "valid": True,
    },
    {
        "id": "missing_width_multibank_pins",
        "signal": {
            "name": "data_bus",
            "multibank": [
                {"bank": 34, "pins": ["P1", "P2"], "offset": 0},
                {"bank": 35, "pins": ["P3", "P4"], "offset": 2},
            ],
            "diff_pair": False,
            "bus": True,
            "direction": "out",
            "buffer": "obuf",
        },
        "validator": validate_multibank_pins,
        "valid": False,
    },
    {
        "id": "valid_multibank_pinset",
        "signal": {
            "name": "diff_data",
            "multibank": [
                {
                    "bank": 34,
                    "pinset": {"p": ["D1", "D2"], "n": ["E1", "E2"]},
                    "offset": 0,
                },
                {
                    "bank": 35,
                    "pinset": {"p": ["D3", "D4"], "n": ["E3", "E4"]},
                    "offset": 2,
                },
            ],
            "diff_pair": True,
            "bus": True,
            "direction": "in",
            "buffer": "ibuf",
            "width": 4,
        },
        "validator": validate_multibank_pinset,
        "valid": True,
    },
    {
        "id": "empty_multibank_section",
        "signal": {
            "name": "empty_multibank",
            "multibank": [],
            "diff_pair": True,
            "bus": True,
            "direction": "in",
            "buffer": "ibuf",
            "width": 2,
        },
        "validator": validate_multibank_pinset,
        "valid": False,
    },
    {
        "id": "mismatched_pinset_lengths",
        "signal": {
            "name": "diff_data",
            "multibank": [
                {"bank": 34, "pinset": {"p": ["D1", "D2"], "n": ["E1"]}, "offset": 0},
                {"bank": 35, "pinset": {"p": ["D3", "D4"], "n": ["E3"]}, "offset": 2},
            ],
            "diff_pair": True,
            "bus": True,
            "direction": "in",
            "buffer": "ibuf",
            "width": 4,
        },
        "validator": validate_multibank_pinset,
        "valid": True,
    },
]


@pytest.mark.parametrize("case", cases, ids=[case["id"] for case in cases])
def test_multibank_validators(case):
    signal = case["signal"]
    validator = case["validator"]
    if case["valid"]:
        validator(signal)
    else:
        with pytest.raises(ValueError):
            validator(signal)
