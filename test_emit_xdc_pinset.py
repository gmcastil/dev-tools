import pytest
from io_gen.emit_xdc import emit_xdc_pinset

cases = [
    {
        "id": "diff_pair",
        "pin": {
            "name": "clk",
            "index": 0,
            "p": "B1",
            "n": "B2",
            "direction": "in",
            "buffer": "ibuf",
            "iostandard": "LVDS"
        },
        "expected": [
            "set_property PACKAGE_PIN B1 [get_ports {clk_p[0]}]",
            "set_property IOSTANDARD LVDS [get_ports {clk_p[0]}]",
            "set_property PACKAGE_PIN B2 [get_ports {clk_n[0]}]",
            "set_property IOSTANDARD LVDS [get_ports {clk_n[0]}]"
        ]
    },
    {
        "id": "diff_pair_index_2",
        "pin": {
            "name": "refclk",
            "index": 2,
            "p": "C1",
            "n": "C2",
            "direction": "in",
            "buffer": "ibuf",
            "iostandard": "LVDS_25"
        },
        "expected": [
            "set_property PACKAGE_PIN C1 [get_ports {refclk_p[2]}]",
            "set_property IOSTANDARD LVDS_25 [get_ports {refclk_p[2]}]",
            "set_property PACKAGE_PIN C2 [get_ports {refclk_n[2]}]",
            "set_property IOSTANDARD LVDS_25 [get_ports {refclk_n[2]}]"
        ]
    }
]

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_emit_xdc_pinset(case):
    result = emit_xdc_pinset(case["pin"])
    assert result == case["expected"]
