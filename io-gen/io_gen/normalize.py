from typing import Any
from copy import deepcopy

from .flatten import flatten_banks, flatten_signals

def normalize(data: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize a validated IO YAML dictionary by flattening its banks and signals.

    This function performs two core transformations:
    1. Calls `flatten_banks()` to convert the list of bank dictionaries into a
       dictionary mapping bank numbers to bank attributes.
    2. Calls `flatten_signals()` to normalize each signal, resolving inherited
       values (e.g., IOSTANDARD from bank) and ensuring a uniform format.

    The original input is not modified; a deep copy is returned with the
    `banks` and `signals` fields replaced by their flattened forms.

    Args:
        data (dict[str, Any]): The validated input dictionary containing the keys
            "title", "part", "banks", and "signals".

    Returns:
        dict[str, Any]: A new dictionary with flattened `banks` (as dict[int, dict])
        and flattened `signals` (as list[dict]).

    Raises:
        ValueError: If a signal is missing an `iostandard` and no matching bank
        exists to inherit it from. Also raises this if there are duplicate bank values.

    """
    normalized = deepcopy(data)  # Copy preserves any other remaining keys

    # Banks need to be flattened first so that signals can properly inherit items
    normalized["banks"] = flatten_banks(data["banks"])
    # Now flatten signals
    normalized["signals"] = flatten_signals(data["signals"], normalized["banks"])

    return normalized

