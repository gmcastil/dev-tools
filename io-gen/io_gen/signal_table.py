from io_gen.utils import *

from typing import Dict, Any, List

def extract_signal_table(signals: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Convert list of signal definitions into a signal table keyed by name.

    This function builds a per-signal metadata table (width, group, comment, etc.)
    based on the signal entries in the YAML. It assumes the input has already
    passed schema validation.

    Args:
        signals: List of signal definitions from the YAML input.

    Returns:
        A dictionary keyed by signal name, where each value contains
        signal-level metadata.

    Raises:
        ValueError - If duplicate signal names are present in the input data

    """
    sig_table = {}

    for sig in signals:
        # First, check for duplciate signal names
        if sig['name'] in sig_table:
            msg = f"Duplicate signal name {sig['name']}"
            raise ValueError(msg)
        else:
            # Signal names are the keys to the signal table
            name = sig['name']

        entry = {}

        # Comment and group for signals are optional
        entry = {
                'group' : sig.get('group', ''),
                'comment' : sig.get('comment', '')
                }

        # The 'as_bus' property needs some careful handling
        if is_pin(sig) or is_pinset_scalar(sig):
            entry['as_bus'] = sig.get('as_bus', False)
        else:
            entry['as_bus'] = False

        # Width is optional for some pin types, which makes it annoying
        # to set properly
        if is_pin(sig) or is_pinset_scalar(sig):
            entry['width'] = sig.get('width', 1)

        # Width is required for pins, pinset arrays and multibank
        elif is_pins(sig) or is_pinset_array(sig) or is_multibank(sig):
            if 'width' in sig:
                entry['width'] = sig['width']
            else:
                msg = f"Signal '{name}' does not have a width property set."
                raise ValueError(msg)

        # Somehow, an unknown signal made its way in here
        # Schena should prevent this from happening
        else:
            msg = f"Signal '{name}' does not a have a pin type"
            raise ValueError(msg)

        sig_table[name] = entry

    return sig_table

def validate_signal_table(signal_table: Dict[str, Dict[str, Any]]) -> None:
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

