import pytest
from io_gen.emit_xdc import emit_xdc_diff

cases = [
    {
        "id": "diff-scalar-wire",
        "pins": [
            {
                "name": "hdmi_clk",
                "index": 0,
                "p": "K2",
                "n": "K1",
                "iostandard": "TMDS_33",
                "buffer": "obuf",
                "direction": "out",
                "width": 1,
                "diff_pair": True,
                "bus": False,
            }
        ],
        "expected": [
            "set_property PACKAGE_PIN K2 [get_ports {hdmi_clk_p}]",
            "set_property IOSTANDARD TMDS_33 [get_ports {hdmi_clk_p}]",
            "set_property PACKAGE_PIN K1 [get_ports {hdmi_clk_n}]",
            "set_property IOSTANDARD TMDS_33 [get_ports {hdmi_clk_n}]",
        ],
    },
    {
        "id": "diff-scalar-bus",
        "pins": [
            {
                "name": "hdmi_clk",
                "index": 0,
                "p": "K2",
                "n": "K1",
                "iostandard": "TMDS_33",
                "buffer": "obuf",
                "direction": "out",
                "width": 1,
                "diff_pair": True,
                "bus": True,
            }
        ],
        "expected": [
            "set_property PACKAGE_PIN K2 [get_ports {hdmi_clk_p[0]}]",
            "set_property IOSTANDARD TMDS_33 [get_ports {hdmi_clk_p[0]}]",
            "set_property PACKAGE_PIN K1 [get_ports {hdmi_clk_n[0]}]",
            "set_property IOSTANDARD TMDS_33 [get_ports {hdmi_clk_n[0]}]",
        ],
    },
    {
        "id": "diff-bus-multibit",
        "pins": [
            {
                "name": "hdmi_data",
                "index": 0,
                "p": "J2",
                "n": "J1",
                "iostandard": "TMDS_33",
                "buffer": "obuf",
                "direction": "out",
                "width": 2,
                "diff_pair": True,
                "bus": True,
            },
            {
                "name": "hdmi_data",
                "index": 1,
                "p": "H2",
                "n": "H1",
                "iostandard": "TMDS_33",
                "buffer": "obuf",
                "direction": "out",
                "width": 2,
                "diff_pair": True,
                "bus": True,
            },
        ],
        "expected": [
            "set_property PACKAGE_PIN J2 [get_ports {hdmi_data_p[0]}]",
            "set_property IOSTANDARD TMDS_33 [get_ports {hdmi_data_p[0]}]",
            "set_property PACKAGE_PIN J1 [get_ports {hdmi_data_n[0]}]",
            "set_property IOSTANDARD TMDS_33 [get_ports {hdmi_data_n[0]}]",
            "set_property PACKAGE_PIN H2 [get_ports {hdmi_data_p[1]}]",
            "set_property IOSTANDARD TMDS_33 [get_ports {hdmi_data_p[1]}]",
            "set_property PACKAGE_PIN H1 [get_ports {hdmi_data_n[1]}]",
            "set_property IOSTANDARD TMDS_33 [get_ports {hdmi_data_n[1]}]",
        ],
    },
]


@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_emit_xdc_diff(case):
    result = emit_xdc_diff(case["pins"])
    assert result == case["expected"]
