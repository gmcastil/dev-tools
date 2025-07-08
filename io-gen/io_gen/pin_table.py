from copy import deepcopy
from typing import Any

from io_gen.utils import *

def extract_pin_table(
    signals: list[dict[str, Any]],
    signal_table: dict[str, dict[str, Any]],
    bank_table: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Flatten pins into atomic entries, grouped per signal.

    This function transforms all signal fragments into a flat list of atomic
    pins or differential pairs. It combines information from signals,
    the signal table, and the bank table.

    Args:
        signals: Raw signal list from YAML.
        signal_table: The extracted per-signal metadata table.
        bank_table: The extracted per-bank metadata table.

    Returns:
        A list of dicts, one per atomic pin or pin pair, each with full metadata.

    """
    pin_table = []

    for sig in signals:

        sig_name = sig['name']
        if is_pin(sig):
            flattened_pins = flatten_signal_pin_scalar(sig, bank_table)
        elif is_pins(sig):
            flattened_pins = flatten_signal_pins_array(sig, bank_table)
        elif is_pinset_scalar(sig):
            flattened_pins = flatten_signal_pinset_scalar(sig, bank_table)
        elif is_pinset_array(sig):
            flattened_pins = flatten_signal_pinset_array(sig, bank_table)
        elif is_multibank(sig):
            flattened_pins = flatten_signal_multibank(sig, bank_table)
        else:
            msg = f"Signal '{sig_name}' has no valid pin definition"
            raise ValueError(msg)

        # Width is a signal property stored in the signal table, but the
        # number of pins isn't known until after flattening. So look up
        # the width in the signal table and compare it to what we got
        # after flattening
        sig_width_from_table = signal_table[sig_name]['width']
        sig_width = len(flattened_pins)
        if sig_width != sig_width_from_table:
            msg = (
                f"Signal '{sig_name}' flattened into {sig_width} entries, "
                f"but signal width was defined as {sig_width_from_table}"
                )
            raise ValueError(msg)

        # Flattened pins have the correct width so we grow the pin table
        pin_table.extend(flattened_pins)
    
    return pin_table

def validate_pin_table(pin_table: dict[str, list[dict[str, Any]]]) -> None:
    """
    Validate the flattened pin table for correctness.

    This includes checks like:
    - Unique (name, index) per signal
    - No reuse of package pins
    - Required metadata fields present

    Args:
        pin_table: The flat list of pins/pairs extracted from signals.

    Raises:
        ValueError: If the pin table violates structural or uniqueness constraints.

    """
    pass

def make_pin_table_entry_stub(signal: dict, banks: dict[int, dict]) -> dict[str, Any]:
    # All pin entries share these
    pin_entry_stub = {
            'name' : signal['name'],
            'direction' : signal['direction'],
            'buffer' : signal['buffer']
            }
    # Now set the iostandard, which may or may not be inherited from the bank
    if "iostandard" not in signal:
        bank = signal.get("bank", None)
        if bank is not None and bank in banks:
            pin_entry_stub['iostandard'] = banks[bank]['iostandard']
        else:
            msg = f"Signal '{signal['name']}' has no bank or IOSTANDARD defined"
            raise ValueError(msg)
    else:
        pin_entry_stub['iostandard'] = signal['iostandard']

    return pin_entry_stub

def flatten_signal_pin_scalar(signal: dict, banks: dict[int, dict]) -> list[dict]:
    """Flatten a single-ended scalar signal into one pin entry."""
    if not is_pin(signal):
        msg = f"Signal '{signal['name']}' is not a scalar pin"
        raise ValueError(msg)

    pin_table_entry = make_pin_table_entry_stub(signal, banks)
    pin_table_entry['pin'] = signal['pin']
    pin_table_entry['index'] = 0

    return [pin_table_entry]

def flatten_signal_pinset_scalar(signal: dict, banks: dict[int, dict]) -> list[dict]:
    """Flatten a differential scalar signal into one pinset entry."""
    if not is_pinset_scalar(signal):
        msg = f"Signal '{signal['name']}' is not a scalar pinset"
        raise ValueError(msg)

    pin_table_entry = make_pin_table_entry_stub(signal, banks)
    pin_table_entry['p'] = signal['pinset']['p']
    pin_table_entry['n'] = signal['pinset']['n']
    pin_table_entry['index'] = 0

    return [pin_table_entry]

def flatten_signal_pins_array(signal: dict, banks: dict[int, dict]) -> list[dict]:
    """Flatten a single-ended array signal into multiple indexed pin entries."""
    if not is_pins(signal):
        msg = f"Signal '{signal['name']}' is not an array of pins"
        raise ValueError(msg)

    result = []
    for index, pin in enumerate(signal['pins']):
        pin_table_entry = make_pin_table_entry_stub(signal, banks)
        pin_table_entry['pin'] = pin
        pin_table_entry['index']  = index
        result.append(pin_table_entry)

    return result

def flatten_signal_pinset_array(signal: dict, banks: dict[int, dict]) -> list[dict]:
    """Flatten a differential array signal into multiple indexed pinset entries."""
    if not is_pinset_array(signal):
        msg = f"Signal '{signal['name']}' is not an array of pinset"
        raise ValueError(msg)

    result = []
    # We don't generally check width here, but we're going to zip these together,
    # which will truncate the trailing values without throwing an exception (3.10+
    # supports a strict mode for zip() but we're not using that). So check the length
    # here and later, we'll check the width like everywhere else.
    p_pins = signal['pinset']['p']
    n_pins = signal['pinset']['n']
    if len(p_pins) != len(n_pins):
        msg = (
            f"Signal '{signal['name']}' has mismatched pinset lengths: "
            f"{len(p_pins)} != {len(n_pins)}"
            )
        raise ValueError(msg)

    for index, (p_pin, n_pin) in enumerate(zip(p_pins, n_pins)):
        pin_table_entry = make_pin_table_entry_stub(signal, banks)
        pin_table_entry['p'] = p_pin
        pin_table_entry['n'] = n_pin
        pin_table_entry['index']  = index
        result.append(pin_table_entry)

    return result

def flatten_signal_multibank(signal: dict, banks: dict[int, dict]) -> list[dict]:
    """Flatten a multibank signal into indexed pin entries across banks."""

    if not is_multibank(signal) or is_mixed_multibank(signal):
        msg = f"Signal '{signal['name']}' is not a multibank or contains mixed pin types"
        raise ValueError(msg)

    # Expressly disallowing the forced single bit bus from multibank buses - these
    # are inherently multi-bit
    if signal.get('as_bus', False):
        msg = f"Signal '{signal['name']}' is multibit and does not support 'as_bus'"
        raise ValueError(msg)

    # Copy this first because we're going to mutate the fragment and turn it into
    # something that resembles a signal
    signal_c = deepcopy(signal)
    result = []
    # Have to keep track of the starting position of each segment - this requires
    # that the banks appear in ascending order of pins
    offset = 0

    for fragment in signal_c['multibank']:
        # To leverage the existing flatten functions, we need to make signal
        # fragments look like signals - this means adding the signal direction
        # buffer type, name, and iostandard (if provided) to the fragment. Each
        # fragment contains the pin or pinset, bank number
        fragment['name'] = signal_c['name']
        fragment['direction'] = signal_c['direction']
        fragment['buffer'] = signal_c['buffer']
        # This can be inherited per-bank but only declared for the top level signal
        if 'iostandard' in signal_c:
            fragment['iostandard'] = signal_c['iostandard']

        if is_pin(fragment):
            flattened = flatten_signal_pin_scalar(fragment, banks)
        elif is_pins(fragment):
            flattened = flatten_signal_pins_array(fragment, banks)
        elif is_pinset_scalar(fragment):
            flattened = flatten_signal_pinset_scalar(fragment, banks)
        elif is_pinset_array(fragment):
            flattened = flatten_signal_pinset_array(fragment, banks)
        else:
            msg = f"Signal '{signal_c['name]']}' has an unknown pin type"
            raise ValueError(msg)

        # Set the index for each elmement of each frragment
        for index, pin in enumerate(flattened, start=offset):
            pin['index'] = index
        offset += len(flattened)

        result.extend(flattened)

    return result

