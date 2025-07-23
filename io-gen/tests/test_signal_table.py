import pytest
import yaml

from io_gen.signal_table import extract_signal_table

test_cases = [
    {
        "id": "minimal_scalar_signal_with_defaults",
        "yaml": """signals:
          - name: led
            pins: A1
            direction: out
            buffer: infer
            width: 1""",
        "expected": [
            {
                "name": "led",
                "direction": "out",
                "buffer": "infer",
                "parameters": {},
                "instance": None,
                "group": "",
                "comment": {},
                "pins": "A1",
                "diff_pair": False,
                "bus": False,
                "width": 1,
            }
        ],
    },
    {
        "id": "bus_signal_array_of_pins_preserved",
        "yaml": """signals:
          - name: data
            pins: [A1, A2, A3]
            direction: in
            buffer: ibuf
            parameters:
              DRIVE: 12
              SLEW: "FAST"
            width: 3""",
        "expected": [
            {
                "name": "data",
                "direction": "in",
                "buffer": "ibuf",
                "parameters": {
                    "SLEW": "FAST",
                    "DRIVE": 12,
                },
                "instance": None,
                "group": "",
                "comment": {},
                "pins": ["A1", "A2", "A3"],
                "diff_pair": False,
                "bus": True,
                "width": 3,
            }
        ],
    },
    {
        "id": "pinset_passed_through",
        "yaml": """signals:
          - name: clk
            pinset:
              p: C1
              n: C2
            direction: in
            buffer: ibuf
            instance: test_clk
            width: 1""",
        "expected": [
            {
                "name": "clk",
                "direction": "in",
                "buffer": "ibuf",
                "parameters": {},
                "instance": "test_clk",
                "group": "",
                "comment": {},
                "pinset": {"p": "C1", "n": "C2"},
                "diff_pair": True,
                "bus": False,
                "width": 1,
            }
        ],
    },
    {
        "id": "preserves_group_and_comment",
        "yaml": """signals:
          - name: rst
            pins: R1
            direction: in
            buffer: ibuf
            group: control
            instance: ext_rst
            comment:
              hdl: active-low reset
            width: 1""",
        "expected": [
            {
                "name": "rst",
                "direction": "in",
                "buffer": "ibuf",
                "parameters": {},
                "instance": "ext_rst",
                "group": "control",
                "comment": {"hdl": "active-low reset"},
                "pins": "R1",
                "diff_pair": False,
                "bus": False,
                "width": 1,
            }
        ],
    },
    {
        "id": "multibank_with_pinset",
        "yaml": """signals:
  - name: diffbus
    multibank:
      - bank: 34
        offset: 0
        pinset:
          p: [C1, C2, C3]
          n: [D1, D2, D3]
      - bank: 35
        offset: 3
        pinset:
          p: [C4, C5, C6]
          n: [D4, D5, D6]
    direction: in
    buffer: ibufds
    parameters:
      DRIVE: 12
      SLEW: FAST
    width: 6""",
        "expected": [
            {
                "name": "diffbus",
                "direction": "in",
                "buffer": "ibufds",
                "parameters": {
                    "DRIVE": 12,
                    "SLEW": "FAST",
                },
                "instance": None,
                "group": "",
                "comment": {},
                "multibank": [
                    {
                        "bank": 34,
                        "offset": 0,
                        "pinset": {"p": ["C1", "C2", "C3"], "n": ["D1", "D2", "D3"]},
                    },
                    {
                        "bank": 35,
                        "offset": 3,
                        "pinset": {"p": ["C4", "C5", "C6"], "n": ["D4", "D5", "D6"]},
                    },
                ],
                "diff_pair": True,
                "bus": True,
                "width": 6,
            }
        ],
    },
]


@pytest.mark.parametrize("case", test_cases, ids=[c["id"] for c in test_cases])
def test_extract_signal_table(case):
    raw = yaml.safe_load(case["yaml"])["signals"]
    result = extract_signal_table(raw)
    assert result == case["expected"]
