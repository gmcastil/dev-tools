from copy import deepcopy

def flatten_signals(signals: list[dict], banks: dict[int, dict]) -> list[dict]:
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

