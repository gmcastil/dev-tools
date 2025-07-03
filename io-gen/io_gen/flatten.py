from copy import deepcopy
from typing import List, Dict, Any

def flatten_signals(signals: List[Dict], banks: Dict[int, Dict]) -> List[Dict]:
    """
    Flatten the list of signals, resolving inheritance from bank definitions.

    Each returned signal dict includes all explicitly provided keys,
    plus inherited 'iostandard' if not overridden.

    Args:
        signals (list): List of signal dictionaries from validated YAML.
        banks (dict): Flattened bank lookup table (bank number -> bank attributes).

    Returns:
        List[dict]: Flat list of resolved signal dictionaries.

    Raises:
        ValueError: If a signal references a bank number not present in the bank list.

    """
    flat = []

    for signal in signals:
        if "pin" in signal:
            flat.extend(flatten_pin(signal, banks))
        elif "pins" in signal:
            flat.extend(flatten_pins(signal, banks))
        elif "pinset" in signal:
            flat.extend(flatten_pinset(signal, banks))
        elif "multibank" in signal:
            flat.extend(flatten_multibank(signal, banks))
        else:
            msg = f"Signal '{signal['name']}' has no valid pin definition"
            raise ValueError(msg)
    
    return flat

def flatten_pin(signal: dict, banks: Dict[int, dict]) -> list[dict]:
    # Going to mangle this and return it, so copy now
    signal_c = deepcopy(signal)

    if 'pin' not in signal_c:
        msg = f"Signal '{signal_c['name']}' has a missing pin value"
        raise ValueError(msg)

    if 'direction' not in signal_c:
        msg = f"Signal '{signal_c['name']}' has a missing direction"
        raise ValueError(msg)

    # Clean up 'bus' if not explicitly true
    if signal_c.get("bus") is not True:
        signal_c.pop("bus", None)

    # Check if the signal itself has the IO standard defined
    if "iostandard" not in signal_c:
        bank = signal_c.get("bank", None)
        if bank is not None and bank in banks:
            signal_c['iostandard'] = banks[bank]['iostandard']
        else:
            msg = f"Signal '{signal_c['name']}' has no bank or IOSTANDARD defined"
            raise ValueError(msg)

    # The index for a single pin is always 0
    signal_c['index'] = 0

    return [signal_c]

def flatten_pins(signal: dict, banks: dict[int, dict]) -> list[dict]:

    flattened = []
    signal_c = deepcopy(signal)

    # Go no further without pins
    if 'pins' not in signal_c:
        msg = f"Signal '{signal_c['name']}' has no pins defined"
        raise ValueError(msg)

    if 'direction' not in signal_c:
        msg = f"Signal '{signal_c['name']}' has a missing direction"
        raise ValueError(msg)

    # Clean up 'bus'  - no reason for this to be here, but get rid of it if it is
    signal_c.pop("bus", None)

    # Now set the iostandard, which may or may not be inherited from the bank
    if 'iostandard' not in signal_c:
        bank = signal_c.get("bank", None)
        if bank is not None and bank in banks:
            signal_c['iostandard'] = banks[bank]['iostandard']
        else:
            msg = f"Signal '{signal_c['name']}' has no bank or IOSTANDARD defined"
            raise ValueError(msg)

    # Will be iterating over the pins, so need to move this list out of the copy
    # before mutating and flattening
    pins = signal_c.pop('pins')

    for index, pin in enumerate(pins):
        signal_cc = deepcopy(signal_c)

        signal_cc['index'] = index
        signal_cc['pin'] = pin

        flattened.append(signal_cc)

    return flattened

def flatten_pinset(signal: dict, banks: dict[int, dict]) -> list[dict]:
    return

def flatten_multibank(signal: dict, banks: dict[int, dict]) -> list[dict]:
    return











    result = []
    for signal in signals:
        signal_copy = deepcopy(signal)  # Copy because we're going to mutate the signal dict

        # The IOSTANDARD property is not required and can be inherited from the bank if not provided
        if "iostandard" not in signal_copy:
            number = signal_copy["bank"]
            if number in banks:
                signal_copy["iostandard"] = banks[number]["iostandard"]
            else:
                raise ValueError(f"Signal '{signal_copy['name']}' refers to undefined bank {number}")
        result.append(signal_copy)
    return result

def flatten_banks(banks: list[dict]) -> dict[int, dict]:
    """
    Flatten a list of bank entries into a lookup dictionary by bank number.

    Each bank must include 'bank', 'iostandard', and 'performance'.
    An optional 'comment' field will be preserved if present.

    Duplicate bank numbers will raise a ValueError.

    Args:
        banks (list): List of bank dictionaries from validated YAML.

    Returns:
        dict[int, dict]: Mapping of bank number to bank attributes.
                         Each value includes at least 'iostandard' and 'performance',
                         and optionally 'comment' if present.

    Raises:
        ValueError: If duplicate bank numbers are detected.

    """
    result = {}

    for bank in banks:
        bank_copy = deepcopy(bank)  # Copy because we're going to mutate the bank dict
        number = bank_copy["bank"]
        # Recall that the keys in the result dict are the bank numbers,
        # so we check for duplicates
        if number in result:
            raise ValueError(f"Found duplicate bank {number} entry")

        # Flattened bank structure is just going to have the bank number
        # removed and used as the key in the result
        del bank_copy["bank"]
        result[number] = bank_copy

    return result

