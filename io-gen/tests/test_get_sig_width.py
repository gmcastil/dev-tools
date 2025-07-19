import pytest
import yaml
from io_gen.utils import get_sig_width

test_cases = [
    {
        "id": "scalar_pin",
        "yaml":"""
signals:
  - name: led
    pins: A1
    direction: out
    buffer: infer
""",
        "expected_width": 1,
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
        "expected_width": 3,
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
""",
        "expected_width": 1,
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
    width: 2
""",
        "expected_width": 2,
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
        "expected_width": 4,
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
        "expected_width": 3,
    },
]

@pytest.mark.parametrize("case", test_cases, ids=[c["id"] for c in test_cases])
def test_get_sig_width(case):
    raw = yaml.safe_load(case["yaml"])["signals"][0]
    assert get_sig_width(raw) == case["expected_width"]
