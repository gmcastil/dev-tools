import pytest
from io_gen.flatten import flatten_pinset

flatten_pinset_cases = [
    {
        "id": "valid_scalar_pinset_differential_pair",
        "valid": True,
        "signal": {
            "name": "clk",
            "direction": "in",
            "buffer": "ibufds",
            "pinset": {
                "p": "C1",
                "n": "C2"
            },
            "bank": 34
        },
        "banks": {
            34: {"iostandard": "DIFF_SSTL15"}
        },
        "expected": [
            {
                "name": "clk",
                "index": 0,
                "p": "C1",
                "n": "C2",
                "bank": 34,
                "direction": "in",
                "buffer": "ibufds",
                "iostandard": "DIFF_SSTL15",
                "bus": False
            }
        ]
    },
    {
        "id": "valid_vector_pinset_differential_pairs",
        "valid": True,
        "signal": {
            "name": "data",
            "direction": "out",
            "buffer": "obufds",
            "pinset": {
                "p": ["D1", "D3"],
                "n": ["D2", "D4"]
            },
            "bank": 35
        },
        "banks": {
            35: {"iostandard": "DIFF_HSTL_I"}
        },
        "expected": [
            {
                "name": "data",
                "index": 0,
                "p": "D1",
                "n": "D2",
                "bank": 35,
                "direction": "out",
                "buffer": "obufds",
                "iostandard": "DIFF_HSTL_I"
            },
            {
                "name": "data",
                "index": 1,
                "p": "D3",
                "n": "D4",
                "bank": 35,
                "direction": "out",
                "buffer": "obufds",
                "iostandard": "DIFF_HSTL_I"
            }
        ]
    },
    {
        "id": "mismatched_pinset_array_lengths_should_fail",
        "valid": False,
        "signal": {
            "name": "broken_diff",
            "direction": "inout",
            "buffer": "iobufds",
            "pinset": {
                "p": ["E1", "E3"],
                "n": ["E2"]
            },
            "bank": 36
        },
        "banks": {
            36: {"iostandard": "DIFF_SSTL15"}
        }
    },
    {
        "id": "missing_pinset_should_fail",
        "valid": False,
        "signal": {
            "name": "ghost_diff",
            "direction": "in",
            "buffer": "ibufds",
            "bank": 34
        },
        "banks": {
            34: {"iostandard": "DIFF_SSTL15"}
        }
    }
]

# --- Test Runner ---

@pytest.mark.parametrize("case", flatten_pinset_cases, ids=[c["id"] for c in flatten_pinset_cases])
def test_flatten_pinset_cases(case):
    if case["valid"]:
        result = flatten_pinset(case["signal"], case["banks"])
        assert result == case["expected"]
    else:
        with pytest.raises(Exception):
            flatten_pinset(case["signal"], case["banks"])
