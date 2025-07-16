import pytest
import yaml
from io_gen.signal_table import form_signal_entry

test_cases = [
    {
        "id": "scalar_pin",
        "yaml": """
signals:
  - name: led
    pins: A1
    direction: out
    buffer: infer
    bank: 34
""",
        "expected": {
            "pins": "A1",
            "direction": "out",
            "buffer": "infer",
            "bank": 34,
            "group": "",
            "comment": {},
            "width": 1,
            "bus": False,
            "diff_pair": False,
        },
    },
    {
        "id": "bus_pin_array",
        "yaml": """
signals:
  - name: data
    pins: [A1, A2, A3]
    direction: in
    buffer: ibuf
    width: 3
""",
        "expected": {
            "pins": ["A1", "A2", "A3"],
            "direction": "in",
            "buffer": "ibuf",
            "group": "",
            "comment": {},
            "width": 3,
            "bus": True,
            "diff_pair": False,
        },
    },
    {
        "id": "scalar_diff_pair",
        "yaml": """
signals:
  - name: clk
    pinset:
      p: C1
      n: C2
    direction: in
    buffer: ibuf
    iostandard: LVCMOS33
""",
        "expected": {
            "pinset": {"p": "C1", "n": "C2"},
            "direction": "in",
            "buffer": "ibuf",
            "iostandard": "LVCMOS33",
            "group": "",
            "comment": {},
            "width": 1,
            "bus": False,
            "diff_pair": True,
        },
    },
    {
        "id": "diff_pair_array",
        "yaml": """
signals:
  - name: diff_bus
    pinset:
      p: [C1, C3]
      n: [C2, C4]
    direction: out
    buffer: obuf
    iostandard: LVCMOS25
    width: 2
""",
        "expected": {
            "pinset": {"p": ["C1", "C3"], "n": ["C2", "C4"]},
            "direction": "out",
            "buffer": "obuf",
            "iostandard": "LVCMOS25",
            "group": "",
            "comment": {},
            "width": 2,
            "bus": True,
            "diff_pair": True,
        },
    },
    {
        "id": "multibank_pin_array",
        "yaml": """
signals:
  - name: ctrl
    multibank:
      - pins: [A1, A2]
        bank: 34
        offset: 0
      - pins: [B1, B2]
        bank: 35
        offset: 2
    direction: out
    buffer: obuf
    width: 4
""",
        "expected": {
            "multibank": [
                {"pins": ["A1", "A2"], "bank": 34, "offset": 0},
                {"pins": ["B1", "B2"], "bank": 35, "offset": 2},
            ],
            "direction": "out",
            "buffer": "obuf",
            "group": "",
            "comment": {},
            "width": 4,
            "bus": True,
            "diff_pair": False,
        },
    },
    {
        "id": "multibank_diff_pair_array",
        "yaml": """
signals:
  - name: clk_diff
    multibank:
      - pinset:
          p: [C1, C3]
          n: [C2, C4]
        bank: 34
        offset: 0
      - pinset:
          p: [D1]
          n: [D2]
        bank: 35
        offset: 2
    direction: in
    buffer: ibuf
    width: 3
""",
        "expected": {
            "multibank": [
                {"pinset": {"p": ["C1", "C3"], "n": ["C2", "C4"]}, "bank": 34, "offset": 0},
                {"pinset": {"p": ["D1"], "n": ["D2"]}, "bank": 35, "offset": 2},
            ],
            "direction": "in",
            "buffer": "ibuf",
            "group": "",
            "comment": {},
            "width": 3,
            "bus": True,
            "diff_pair": True,
        },
    },
]

@pytest.mark.parametrize("case", test_cases, ids=[c["id"] for c in test_cases])
def test_form_signal_entry(case):
    raw = yaml.safe_load(case["yaml"])["signals"][0]
    result = form_signal_entry(raw)
    assert result == case["expected"]
