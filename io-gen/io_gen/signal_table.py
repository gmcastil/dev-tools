from typing import Any
from copy import copy, deepcopy

from io_gen.utils import *

def extract_signal_table(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert list of signal definitions into a signal table keyed by name.

    This function builds a per-signal metadata table (width, group, comment, etc.)
    based on the signal entries in the YAML. It assumes the input has already
    passed schema validation.

    Args:
        signals: List of signal definitions from the YAML input.

    Returns:
        list of dict

    Raises:
        ValueError - If duplicate signal names are present in the input data

    """
    sig_table = []
    sig_names = set()

    for sig in signals:

        # Skip omitted signals
        if not sig.get('generate', True):
            continue

        # Check for duplciate signal names
        name = sig['name']
        if name in sig_names:
            msg = f"Duplicate signal name '{name}'"
            raise ValueError(msg)
        else:
            sig_names.add(name)

        # No reason to keep dragging these generate = true keys around everywhere
        sig.pop('generate', None)
        sig_table.append(form_signal_entry(sig))

    return sig_table

def form_signal_entry(signal: dict[str, Any]) -> dict[str, Any]:
    """Creates a signal table entry from a YAML entry"""

    # These fields are required by the schema (for signals that will be
    # added to the table)
    entry = {
        'name' : signal['name'],
        'direction' : signal['direction'],
        'buffer' : signal['buffer']
    }

    # Comment and group for signals are optional
    entry['group'] = signal.get('group', "")
    # Signals contain structured comments so just leave this empty if none provided
    entry['comment'] = signal.get('comment', {})

    # Recall that 'iostandard' is an optional property for the entire
    # signal (including multibank - multibank signals can specify the
    # IOSTANDARD property for the entire signal or inherit per bank)
    if 'iostandard' in signal:
        entry['iostandard'] = signal['iostandard']

    # Per the schema, bank is required for multibank signals (so when we
    # deepcopy it later we'll get the banks) but is optional for other
    # kinds of signals so that we can inherit the 'iostandard' per bank.
    if not is_multibank_pinset(signal) and not is_multibank_pins(signal):
        if 'bank' in signal:
            entry['bank'] = signal['bank']

    # Determine pin type
    if is_scalar_pins(signal):
        entry['pins'] = deepcopy(signal['pins'])
        entry['diff_pair'] = False
        entry['bus'] = False
    elif is_scalar_pinset(signal):
        entry['pinset'] = deepcopy(signal['pinset'])
        entry['diff_pair'] = True
        entry['bus'] = False
    elif is_array_pins(signal):
        entry['pins'] = deepcopy(signal['pins'])
        entry['diff_pair'] = False
        entry['bus'] = True
    elif is_array_pinset(signal):
        entry['pinset'] = deepcopy(signal['pinset'])
        entry['diff_pair'] = True
        entry['bus'] = True
    elif is_multibank_pins(signal):
        entry['multibank'] = deepcopy(signal['multibank'])
        entry['diff_pair'] = False
        entry['bus'] = True
    elif is_multibank_pinset(signal):
        entry['multibank'] = deepcopy(signal['multibank'])
        entry['diff_pair'] = True
        entry['bus'] = True
    else:
        msg = f"Signal '{signal['name']}' has missing or malformed pin definition"
        raise ValueError(msg)

    entry['width'] = get_sig_width(signal)

    return entry

def validate_signal_table(signal_table: dict[str, dict[str, Any]]) -> None:
    """
    Validate the signal table for internal consistency.

    This ensures that each signal entry includes all required fields.

    Args:
        signal_table: The extracted signal metadata table.

    Raises:
        ValueError: If any signal entry is missing required fields.
    """
    REQUIRED_FIELDS = {"width", "group", "comment", "as_bus"}

    for name, entry in signal_table.items():
        missing = REQUIRED_FIELDS - set(entry.keys())
        if missing:
            msg = (
                f"Signal '{name}' is missing required fields: {sorted(missing)}"
            )
            raise ValueError(msg)

