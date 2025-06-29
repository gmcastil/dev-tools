def normalize(data: dict) -> dict:
    """
    Normalize the top-level YAML structure by flattening signals and banks.

    This function:
    - Replaces 'banks' with a lookup dictionary (bank number -> bank attributes)
    - Replaces 'signals' with a list of fully resolved signal entries
    - Preserves all other top-level fields (e.g. title, part, metadata)

    Args:
        data (dict): Validated YAML input matching the schema.

    Returns:
        dict: A normalized copy of the input data, with 'signals' and 'banks' flattened.

    """
    normalized = dict(data)  # Shallow copy preserves any other remaining keys

    # Banks need to be flattened first so that signals can properly inherit items
    normalized["banks"] = flatten_banks(data["banks"])
    # Now flatten signals
    normalized["signals"] = flatten_signals(data["signals"], normalized["banks"])

    return normalized

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

        # The IOSTANDARD property is not required and can be inherited from the bank if not provided
        if "iostandard" not in signal:
            number = signal["bank"]
            if number in banks:
                signal["iostandard"] = banks[number]["iostandard"]
            else:
                raise ValueError(f"Signal '{signal['name']}' refers to undefined bank {number}")
        result.append(signal)
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
        number = bank["bank"]
        # Recall that the keys in the result dict are the bank numbers,
        # so we check for duplicates
        if number in result:
            raise ValueError(f"Found duplicate bank {number} entry")

        # Flattened bank structure is just going to have the bank number
        # removed and used as the key in the result
        del bank["bank"]
        result[number] = bank

    return result

