import pytest
from copy import deepcopy
from io_gen.flatten import flatten_multibank

test_cases = [
    {
        "id": "missing_offset",
        "valid": False,
        "signal": {
            "name": "bad_signal1",
            "direction": "in",
            "buffer": "ibuf",
            "width": 2,
            "multibank": [
                {
                    "bank": 34,
                    "pins": ["A1", "A2"]
                }
            ]
        },
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33"}
        ]
    },
    {
        "id": "missing_width",
        "valid": False,
        "signal": {
            "name": "bad_signal2",
            "direction": "in",
            "buffer": "ibuf",
            "multibank": [
                {
                    "bank": 34,
                    "offset": 0,
                    "pins": ["A1", "A2"]
                }
            ]
        },
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33"}
        ]
    },
    {
        "id": "incorrect_offset_overlap",
        "valid": False,
        "signal": {
            "name": "bad_signal3",
            "direction": "in",
            "buffer": "ibuf",
            "width": 4,
            "multibank": [
                {
                    "bank": 34,
                    "offset": 0,
                    "pins": ["A1", "A2"]
                },
                {
                    "bank": 34,
                    "offset": 1,
                    "pins": ["A3", "A4"]
                }
            ]
        },
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33"}
        ]
    },
    {
        "id": "incorrect_total_width_mismatch",
        "valid": False,
        "signal": {
            "name": "bad_signal4",
            "direction": "in",
            "buffer": "ibuf",
            "width": 3,
            "multibank": [
                {
                    "bank": 34,
                    "offset": 0,
                    "pins": ["A1", "A2"]
                },
                {
                    "bank": 35,
                    "offset": 2,
                    "pins": ["B1", "B2"]
                }
            ]
        },
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33"},
            {"bank": 35, "iostandard": "LVCMOS33"}
        ]
    },
    {
        "id": "reversed_offsets",
        "valid": False,
        "signal": {
            "name": "bad_signal5",
            "direction": "in",
            "buffer": "ibuf",
            "width": 4,
            "multibank": [
                {
                    "bank": 35,
                    "offset": 2,
                    "pins": ["B1", "B2"]
                },
                {
                    "bank": 34,
                    "offset": 0,
                    "pins": ["A1", "A2"]
                }
            ]
        },
        "banks": [
            {"bank": 34, "iostandard": "LVCMOS33"},
            {"bank": 35, "iostandard": "LVCMOS33"}
        ]
    }
]

@pytest.mark.parametrize("case", test_cases, ids=[c["id"] for c in test_cases])
def test_flatten_multibank_invalid(case):
    signal = deepcopy(case["signal"])
    banks = {b["bank"]: b for b in case["banks"]}

    with pytest.raises(ValueError):
        flatten_multibank(signal, banks)
