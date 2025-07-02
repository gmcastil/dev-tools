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

    This function determines the signal's bit width based on its physical
    structure:
        - 'pin': scalar -> width = 1
        - 'pins': list of pin names -> width = len(pins)
        - 'pinset': differential pair
          - If 'p' and 'n' are both strings -> width = 1
          - If 'p' and 'n' are both lists of equal length -> width = len(p)

    The returned dictionary includes a new 'width' field but otherwise
    preserves the original signal structure. Note that this function does
    not use the `bus` property - that property is used later when checking
    the annotated data prior to generating HDL.

    Raises:
        ValueError: If 'pinset' uses mismatched types or unequal lengths,
                    or if no supported pin field is found.

    Returns:
        dict: A copy of the signal with the 'width' field added.

    """
    signal_a = deepcopy(signal)

    if "pin" in signal_a:
        # Unambigously scalar (might be a bus, but irrelevant here)
        signal_a["width"] = 1
    elif "pins" in signal_a:
        # Unambiguously a vector
        signal_a["width"] = len(signal_a["pins"])
    elif "pinset" in signal_a:
        # Schema cannot validate that p and n are both strings or lists,
        # so we check the types and raise here and set the width depending
        # on whether we have arrays or strings.
        pinset = signal_a['pinset']
        n = pinset['n']
        p = pinset['p']
        if type(n) != type(p):
            raise ValueError(
                f"Signal '{signal_a['name']}' has mismatched pinset types: "
                f"'p' is {type(p).__name__}, 'n' is {type(n).__name__}. "
                "Both must be either strings or lists of equal length."
            )

        # Lengths of n and p lists need to match
        if isinstance(p, list):
            p_len = len(pinset['p'])
            n_len = len(pinset['n'])
            if p_len != n_len:
                raise ValueError(
                        f"Signal '{signal_a['name']}' must be equal lengths. "
                        f"'p' has length {len(p)}, 'n' has length {len(n)}."
                        )
            else:
                signal_a["width"] = len(p)
        # Strings can only have a width of 1
        elif isinstance(p, str):
            signal_a["width"] = 1
        # This should violate the schema requirements
        else:
            raise ValueError(
                    f"Signal '{signal_a['name']}' has an unknown type"
                    )
    # This would violate the schema requirements too
    else:
        raise ValueError(
                f"Signal '{signal_a['name']}' has missing pin definitions"
                )

    return signal_a

