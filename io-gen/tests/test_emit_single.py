import pytest
from io_gen.emit_xdc import emit_xdc_single

cases = [
    {
        "id": "scalar-wire",
        "pins": [
            {
                "name": "btn",
                "index": 0,
                "pin": "A9",
                "iostandard": "LVCMOS33",
                "buffer": "ibuf",
                "direction": "in",
                "width": 1,
                "diff_pair": False,
                "bus": False,
            }
        ],
        "expected": [
            "set_property PACKAGE_PIN A9 [get_ports {btn_pad}]",
            "set_property IOSTANDARD LVCMOS33 [get_ports {btn_pad}]",
        ],
    },
    {
        "id": "scalar-bus",
        "pins": [
            {
                "name": "btn",
                "index": 0,
                "pin": "A9",
                "iostandard": "LVCMOS33",
                "buffer": "ibuf",
                "direction": "in",
                "width": 1,
                "diff_pair": False,
                "bus": True,
            }
        ],
        "expected": [
            "set_property PACKAGE_PIN A9 [get_ports {btn_pad[0]}]",
            "set_property IOSTANDARD LVCMOS33 [get_ports {btn_pad[0]}]",
        ],
    },
    {
        "id": "bus-multibit",
        "pins": [
            {
                "name": "sw",
                "index": 0,
                "pin": "A1",
                "iostandard": "LVCMOS18",
                "buffer": "ibuf",
                "direction": "in",
                "width": 2,
                "diff_pair": False,
                "bus": True,
            },
            {
                "name": "sw",
                "index": 1,
                "pin": "A2",
                "iostandard": "LVCMOS18",
                "buffer": "ibuf",
                "direction": "in",
                "width": 2,
                "diff_pair": False,
                "bus": True,
            },
        ],
        "expected": [
            "set_property PACKAGE_PIN A1 [get_ports {sw_pad[0]}]",
            "set_property IOSTANDARD LVCMOS18 [get_ports {sw_pad[0]}]",
            "set_property PACKAGE_PIN A2 [get_ports {sw_pad[1]}]",
            "set_property IOSTANDARD LVCMOS18 [get_ports {sw_pad[1]}]",
        ],
    },
]


@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_emit_xdc_single(case):
    result = emit_xdc_single(case["pins"])
    assert result == case["expected"]
