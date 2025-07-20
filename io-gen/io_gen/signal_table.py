import logging

logger = logging.getLogger(__name__)

from copy import deepcopy
from typing import Any

from io_gen.utils import (
    get_sig_width,
    is_array_pins,
    is_array_pinset,
    is_multibank_pins,
    is_multibank_pinset,
    is_scalar_pins,
    is_scalar_pinset,
)


def extract_signal_table(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert list of signal definitions into a signal table keyed by name.

    This function builds a per-signal metadata table (width, group, comment, etc.) based
    on the signal entries in the YAML. It assumes the input has already passed schema
    validation.

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
        if not sig.get("generate", True):
            continue

        # Check for duplciate signal names
        logger.debug("Checking for duplicates")
        name = sig["name"]
        if name in sig_names:
            msg = f"Duplicate signal name '{name}'"
            raise ValueError(msg)
        else:
            sig_names.add(name)

        # No reason to keep dragging these generate = true keys around everywhere
        sig.pop("generate", None)
        sig_table.append(form_signal_entry(sig))

    return sig_table


def form_signal_entry(signal: dict[str, Any]) -> dict[str, Any]:
    """Creates a signal table entry from a YAML entry"""

    # These fields are required by the schema (for signals that will be
    # added to the table)
    entry = {
        "name": signal["name"],
        "direction": signal["direction"],
        "buffer": signal["buffer"],
    }

    # Comment and group for signals are optional
    entry["group"] = signal.get("group", "")
    # Signals contain structured comments so just leave this empty if none provided
    entry["comment"] = signal.get("comment", {})

    # Recall that 'iostandard' is an optional property for the entire
    # signal (including multibank - multibank signals can specify the
    # IOSTANDARD property for the entire signal or inherit per bank)
    if "iostandard" in signal:
        entry["iostandard"] = signal["iostandard"]

    # Per the schema, bank is required for multibank signals (so when we
    # deepcopy it later we'll get the banks) but is optional for other
    # kinds of signals so that we can inherit the 'iostandard' per bank.
    if not is_multibank_pinset(signal) and not is_multibank_pins(signal):
        if "bank" in signal:
            entry["bank"] = signal["bank"]

    # Determine pin type
    if is_scalar_pins(signal):
        entry["pins"] = deepcopy(signal["pins"])
        entry["diff_pair"] = False
        entry["bus"] = False
    elif is_scalar_pinset(signal):
        entry["pinset"] = deepcopy(signal["pinset"])
        entry["diff_pair"] = True
        entry["bus"] = False
    elif is_array_pins(signal):
        entry["pins"] = deepcopy(signal["pins"])
        entry["diff_pair"] = False
        entry["bus"] = True
    elif is_array_pinset(signal):
        entry["pinset"] = deepcopy(signal["pinset"])
        entry["diff_pair"] = True
        entry["bus"] = True
    elif is_multibank_pins(signal):
        entry["multibank"] = deepcopy(signal["multibank"])
        entry["diff_pair"] = False
        entry["bus"] = True
    elif is_multibank_pinset(signal):
        entry["multibank"] = deepcopy(signal["multibank"])
        entry["diff_pair"] = True
        entry["bus"] = True
    else:
        msg = f"Signal '{signal['name']}' has missing or malformed pin definition"
        raise ValueError(msg)

    entry["width"] = get_sig_width(signal)

    return entry


def get_signal_names(signal_table: list[dict[str, Any]]) -> list[str]:
    """Returns a list of signal names from the signal table"""
    return list(set(sig["name"] for sig in signal_table))
