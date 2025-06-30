# io_gen/annotate.py

from copy import deepcopy

def annotate(data: dict) -> dict:
    """Add computed fields like width to normalized signals."""
    annotated = deepcopy(data)
    annotated["signals"] = [annotate_width(sig) for sig in data["signals"]]
    return annotated

def annotate_width(signal: dict) -> dict:
    """
    Annotate a signal dictionary with a computed 'width' field.

    This function interprets the signal's physical description 
    (pin, pins, or pinset) along with the optional 'bus' boolean 
    to determine how many bits wide the signal is.

    Valid signal formats:
    - 'pin': Single pin name → width = 1
    - 'pins': List of 2+ pin names → width = len(pins)
    - 'pinset': Dict with keys 'p' and 'n' (for differential pairs)
        • If both are strings → width = 1
        • If both are lists → width = len(p)
          (must match length of 'n'; must match type)
        • If both are lists of length 1 and 'bus': true → width = 1
          (explicit 1-bit bus)
        • All mismatched types, lengths, or ambiguous 1-bit cases 
          without 'bus' raise ValueError

    This function raises:
        ValueError: If signal structure is invalid or mismatched
                    (e.g., pinset lengths or types don't match)

    Returns:
        A new copy of the signal dict, with 'width' added.
    """

