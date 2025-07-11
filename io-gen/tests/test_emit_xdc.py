import pytest
from io_gen.emit_xdc import (
    emit_signal_xdc,
    emit_single_ended_xdc,
    emit_diff_pair_xdc,
    emit_as_single_bit_signal
)

# --- Test Fixtures ---

single_ended = {
    "name": "led",
    "index": 0,
    "pin": "A1",
    "bank": 34,
    "direction": "out",
    "buffer": "obuf",
    "iostandard": "LVCMOS33",
    "scalar_as_bus": False
}

differential = {
    "name": "clk_diff",
    "index": 0,
    "p": "B1",
    "n": "B2",
    "bank": 34,
    "direction": "in",
    "buffer": "ibuf",
    "iostandard": "LVDS",
    "scalar_as_bus": False
}

