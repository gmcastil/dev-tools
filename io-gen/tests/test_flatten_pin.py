import pytest
from io_gen.flatten import flatten_pin

# --- Test Cases ---

flatten_pin_cases = [
        {
            "id": "basic_pin_inherits_iostandard",
            "valid": True,
            "signal": {
                "name": "led",
                "direction": "out",
                "buffer": "obuf",
                "pin": "A1",
                "bank": 34,
                "bus": False
                },
            "banks": {
                34: {"iostandard": "LVCMOS33"}
                },
            "expected": [
                {
                    "name": "led",
                    "index": 0,
                    "pin": "A1",
                    "bank": 34,
                    "direction": "out",
                    "buffer": "obuf",
                    "iostandard": "LVCMOS33",
                    "bus": False
                    }
                ]
            },
        {
            "id": "explicit_iostandard_overrides_bank",
            "valid": True,
            "signal": {
                "name": "led",
                "direction": "out",
                "buffer": "obuf",
                "pin": "A1",
                "bank": 34,
                "iostandard": "SSTL15"
                },
            "banks": {
                34: {"iostandard": "LVCMOS33"}
                },
            "expected": [
                {
                    "name": "led",
                    "index": 0,
                    "pin": "A1",
                    "bank": 34,
                    "direction": "out",
                    "buffer": "obuf",
                    "iostandard": "SSTL15",
                    "bus": False
                    }
                ]
            },
    {
            "id": "scalar_bus_true_should_include_flag",
            "valid": True,
            "signal": {
                "name": "flag",
                "direction": "in",
                "buffer": "ibuf",
                "pin": "B1",
                "bank": 35,
                "bus": True
                },
            "banks": {
                35: {"iostandard": "LVCMOS12"}
                },
            "expected": [
                {
                    "name": "flag",
                    "index": 0,
                    "pin": "B1",
                    "bank": 35,
                    "direction": "in",
                    "buffer": "ibuf",
                    "iostandard": "LVCMOS12",
                    "bus": True
                    }
                ]
            },
    {
            "id": "missing_bank_entry_should_fail",
            "valid": False,
            "signal": {
                "name": "status",
                "direction": "in",
                "buffer": "ibuf",
                "pin": "Z1",
                "bank": 99
                },
            "banks": {
                34: {"iostandard": "LVCMOS33"}
                }
            },
    {
            "id": "missing_pin_should_fail",
            "valid": False,
            "signal": {
                "name": "ready",
                "direction": "in",
                "buffer": "ibuf",
                "bank": 34
                },
            "banks": {
                34: {"iostandard": "LVCMOS33"}
                }
            },
    {
            "id": "missing_direction_should_fail",
            "valid": False,
            "signal": {
                "name": "mode",
                "buffer": "obuf",
                "pin": "Y1",
                "bank": 34
                },
            "banks": {
                34: {"iostandard": "LVCMOS33"}
                }
            }
]

@pytest.mark.parametrize("case", flatten_pin_cases, ids=[c["id"] for c in flatten_pin_cases])
def test_flatten_pin_cases(case):
    if case["valid"]:
        result = flatten_pin(case["signal"], case["banks"])
        assert result == case["expected"]
    else:
        with pytest.raises(Exception):
            flatten_pin(case["signal"], case["banks"])
