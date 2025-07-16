from typing import Any

from utils import is_scalar_pins, is_array_pins
from utils import is_scalar_pinset, is_array_pinset
from utils import is_multibank_pins, is_multibank_pinset

def extract_pin_table(
    signal_table: dict[str, dict[str, Any]],
    bank_table: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Flatten signals into atomic pin entries

    This function transforms all signal definitions into a flat list of atomic
    pins or differential pairs.

    Args:
        signal_table: The extracted per-signal metadata table, with keys as signal names
        bank_table: The extracted per-bank metadata table, with keys as bank numbers

    Returns:
        A list of dicts, one per atomic pin or pin pair, each with full metadata.

    """
    pin_table = []

    for sig_name in signal_table:
        signal = signal_table[sig_name]

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

def flatten_scalar_pins(signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    """Flattens a signal into a list of pins"""

    entry = get_pin_table_entry(signal, bank_table)
    entry['index'] = 0
    entry['pin'] = signal['pins']
    pin_table_entries = [entry]

    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries

def flatten_array_pins(signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    """Flattens a signal into a list of pins"""

    pin_table_entries = []
    for index, pin in enumerate(signal['pins']):
        entry = get_pin_table_entry(signal, bank_table)
        entry['index'] = index
        entry['pin'] = pin
        pin_table_entries.append(entry)
    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries

def flatten_scalar_pinset(signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    """Flattens a signal into a list of pin pairs"""
    assert signal['diff_pair'], f"Signal '{signal['name']}' is not a differential pair"

    entry = get_pin_table_entry(signal, bank_table)
    entry['index'] = 0
    entry['p'] = signal['p']
    entry['n'] = signal['n']
    pin_table_entries = [entry]

    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries

def flatten_array_pinset(signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    """Flattens a signal into a list of pin pairs"""
    assert signal['diff_pair'], f"Signal '{signal['name']}' is not a differential pair"

    pin_table_entries = []
    for index, (pin_p, pin_n) in enumerate(zip(signal["pinset"]["p"], signal["pinset"]["n"])):
        entry = get_pin_table_entry(signal, bank_table)
        entry['index'] = index
        entry['p'] = pin_p
        entry['n'] = pin_n
        pin_table_entries.append(entry)

    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries

def flatten_multibank_pins(signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    assert 'multibank' in signal, f"Signal '{signal['name']}' is not a multibank signal"

def flatten_multibank_pinset(signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    assert 'multibank' in signal, f"Signal '{signal['name']}' is not a multibank signal"

def get_pin_table_entry(signal: dict[str, Any], bank_table dict[int, dict[str, Any]]) -> dict[str, Any]:
    """Returns a minimal pin table entry with name, direction, buffer, and iostandard

    Args:
        signal - Entry from the signal table to use as a starting point for a pin table entry
        bank_table - Bank table

    Returns:
        dict

    """
    # Every entry in the pin table will get these values directly fro the signal its a part of
    entry = {
        'name' : signal['name'],
        'direction' : signal['direction'],
        'buffer' : signal['buffer'],
        'diff_pair' : signal['diff_pair'],
        'bus' : signal['bus']
    }

    # The iostandard is a bit more sophisticated, so resolve that separately
    entry['iostandard'] = resolve_iostandard(signal, bank_table)

    return entry

def resolve_iostandard(signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]) -> str:
    """Resolves the iostandard for a signal via inheritance or direct specification"""

    # The iostandard is specified directly (but checked if a bank was supplied)
    if 'iostandard' in signal:
        sig_iostandard = signal['iostandard']

        if 'bank' in signal:
            bank_iostandard = get_bank_iostandard(signal['bank'], bank_table)
            if bank_iostandard != sig_iostandard:
                msg = (
                    f"Signal '{signal['name']}' specifies IOSTANDARD '{sig_iostandard}' but bank {signal['bank']} declares "
                    f"'{bank_iostandard}' — values must match. Either remove the signal-level IOSTANDARD to "
                    f"inherit from the bank, or update one to resolve the conflict."
                    )
                raise ValueError(msg)
    # The iostandard is inherited
    elif 'bank' in signal:
        sig_iostandard = get_bank_iostandard(signal['bank'], bank_table)
    # Cannot resolve the iostandard
    else:
        msg = f"Signal '{signal['name']}' does not contain an 'iostandard' or 'bank' property"
        raise ValueError(msg)

    return sig_iostandard

def get_bank_iostandard(number: int, bank_table: dict[int, dict[str, Any]]) -> str:
    """Looks up the IOSTANDARD property for a bank from the bank table"""

    if number not in bank_table:
        msg = f"Bank table does not contain an entry for bank {number}"
        raise ValueError(msg)

    # The bank 'iostandard' key is required by the schema
    assert 'iostandard' in bank_table[number], "Bank 'iostandard' is missing from bank table entry"

    iostandard = bank_table[number]['iostandard']
    return iostandard

def check_flattened_width(signal: dict[str, Any], pin_entries: list[dict[str, Any]]) -> None:
    """Checks that flattened pin entries have the appropriate width and range"""

    actual_indices = sorted(entry['index'] for entry in pin_entries)
    expected_indices = list(range(0, signal['width']))

    if actual_indices != expected_indices:
        msg = (
                f"Signal '{signal['name']}' has index or width mismatch: "
                f"expected {expected_indices}, but got {actual_indices}"
                )
        raise ValueError(msg)
    

