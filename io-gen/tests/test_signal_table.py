import pytest
import yaml
from io_gen.signal_table import extract_signal_table

test_cases = [
    {
        "id": "minimal_scalar_signal_with_defaults",
        "yaml": """
        signals:
          - name: led
            pins: A1
            direction: out
            buffer: infer
        """,
        "expected": [
            {
                "name": "led",
                "pins": "A1",
                "direction": "out",
                "buffer": "infer",
                "group": "",
                "comment": "",
            }
        ]
    },
    {
        "id": "bus_signal_array_of_pins_preserved",
        "yaml": """
        signals:
          - name: data
            pins: [A1, A2, A3]
            direction: in
            buffer: ibuf
        """,
        "expected": [
            {
                "name": "data",
                "pins": ["A1", "A2", "A3"],
                "direction": "in",
                "buffer": "ibuf",
                "group": "",
                "comment": "",
            }
        ]
    },
    {
        "id": "pinset_passed_through",
        "yaml": """
        signals:
          - name: clk
            pinset:
              p: C1
              n: C2
            direction: in
            buffer: ibuf
        """,
        "expected": [
            {
                "name": "clk",
                "pinset": {"p": "C1", "n": "C2"},
                "direction": "in",
                "buffer": "ibuf",
                "group": "",
                "comment": "",
            }
        ]
    },
    {
        "id": "preserves_group_and_comment",
        "yaml": """
        signals:
          - name: rst
            pins: R1
            direction: in
            buffer: ibuf
            group: control
            comment: active-low reset
        """,
        "expected": [
            {
                "name": "rst",
                "pins": "R1",
                "direction": "in",
                "buffer": "ibuf",
                "group": "control",
                "comment": "active-low reset",
            }
        ]
    },
]

@pytest.mark.parametrize("case", test_cases, ids=[c["id"] for c in test_cases])
def test_extract_signal_table(case):
    raw = yaml.safe_load(case["yaml"])["signals"]
    result = extract_signal_table(raw)
    assert result == case["expected"]

