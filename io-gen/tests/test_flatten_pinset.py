import pytest
from copy import deepcopy

from io_gen.flatten import flatten_pinset
from tests.utils import assert_flat_signals_equal

pinset_test_cases = [
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
                "as_bus": False
            }
        ]
    },
    {
        "id": "valid_scalar_pinset_differential_pair_as_bus",
        "valid": True,
        "signal": {
            "name": "clk_as_bus",
            "direction": "in",
            "buffer": "ibufds",
            "pinset": {
                "p": "C1",
                "n": "C2"
            },
            "bank": 34,
            "as_bus": True
        },
        "banks": {
            34: {"iostandard": "DIFF_SSTL15"}
        },
        "expected": [
            {
                "name": "clk_as_bus",
                "index": 0,
                "p": "C1",
                "n": "C2",
                "bank": 34,
                "direction": "in",
                "buffer": "ibufds",
                "iostandard": "DIFF_SSTL15",
                "as_bus": True
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
                "as_bus": False,
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
                "as_bus": False,
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

test_ids = [c["id"] for c in pinset_test_cases]

@pytest.mark.parametrize("case", pinset_test_cases, ids=test_ids)
def test_flatten_pinset_cases(case):
    signal = deepcopy(case["signal"])
    banks = case['banks']

    if case["valid"]:
        result = flatten_pinset(signal, banks)
        assert_flat_signals_equal(result, case['expected'])
    else:
        with pytest.raises(Exception):
            flatten_pinset(case["signal"], case["banks"])
