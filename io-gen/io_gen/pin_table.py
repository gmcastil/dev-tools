from typing import Any

from io_gen.utils import (
    is_array_pins,
    is_array_pinset,
    is_multibank_pins,
    is_multibank_pinset,
    is_scalar_pins,
    is_scalar_pinset,
)

from io_gen.flatten import (
    flatten_scalar_pins,
    flatten_array_pins,
    flatten_scalar_pinset,
    flatten_array_pinset,
    flatten_multibank_pins,
    flatten_multibank_pinset,
)


def extract_pin_table(
    signal_table: list[dict[str, Any]], bank_table: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Flatten signals into atomic pin entries

    This function transforms all signal definitions into a flat list of atomic
    pins or differential pairs.

    Args:
        signal_table: The extracted per-signal metadata table
        bank_table: The extracted per-bank metadata table, with keys as bank numbers

    Returns:
        A list of dicts, one per atomic pin or pin pair, each with full metadata.

    """
    pin_table = []

    for signal in signal_table:
        if is_scalar_pins(signal):
            pin_entries = flatten_scalar_pins(signal, bank_table)
        elif is_array_pins(signal):
            pin_entries = flatten_array_pins(signal, bank_table)
        elif is_scalar_pinset(signal):
            pin_entries = flatten_scalar_pinset(signal, bank_table)
        elif is_array_pinset(signal):
            pin_entries = flatten_array_pinset(signal, bank_table)
        elif is_multibank_pins(signal):
            pin_entries = flatten_multibank_pins(signal, bank_table)
        elif is_multibank_pinset(signal):
            pin_entries = flatten_multibank_pinset(signal, bank_table)
        else:
            msg = f"Signal '{signal['name']}' has unknown pin type"
            raise ValueError(msg)

        pin_table.extend(pin_entries)

    return pin_table


def get_pins_by_signal(
    name: str, pin_table: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Groups and returns flattened pins from the pin table sorted by index"""

    pins = [entry for entry in pin_table if entry["signal"] == name]
    if not pins:
        msg = f"No pins found for signal '{name}'"
        raise ValueError(msg)

    return sorted(pins, key=lambda entry: entry["index"])
