import pytest
from io_gen.emit_xdc import emit_xdc_pin

cases = [
    {
        "id": "simple_pin",
        "pin": {
            "name": "led",
            "index": 0,
            "pin": "A1",
            "direction": "out",
            "buffer": "obuf",
            "iostandard": "LVCMOS33"
        },
        "expected": [
            "set_property PACKAGE_PIN A1 [get_ports {led[0]}]",
            "set_property IOSTANDARD LVCMOS33 [get_ports {led[0]}]"
        ]
    },
    {
        "id": "pin_index_3",
        "pin": {
            "name": "data",
            "index": 3,
            "pin": "A4",
            "direction": "in",
            "buffer": "ibuf",
            "iostandard": "LVCMOS18"
        },
        "expected": [
            "set_property PACKAGE_PIN A4 [get_ports {data[3]}]",
            "set_property IOSTANDARD LVCMOS18 [get_ports {data[3]}]"
        ]
    }
]

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_emit_xdc_pin(case):
    result = emit_xdc_pin(case["pin"])
    assert result == case["expected"]
