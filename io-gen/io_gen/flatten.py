"""
Flatten and normalize validated input data before generating HDL or XDC

Responsibilities:
- Transform structured YAML data into a flat list of signal descriptions.
- Attach bank defaults (e.g. IOSTANDARD) to each signal.
- Validate logical consistency (e.g., pad required for non-internal signals).

Input:
- Validated dict from `validator`

Output:
- List of dict with each entry a discrete signal that is ready for emission

"""




def flatten_signals(data: dict) -> list[dict]:
    """
    Flatten the list of signals, resolving inheritance from bank definitions.

    Each returned signal dict includes all explicitly provided keys, plus inherited 'iostandard' if not overridden.

    Args:
        data (dict): Validated input data matching the schema.

    Returns:
        List[dict]: Flat list of resolved signal dictionaries.

    """
    pass

def flatten_banks(data: dict) -> list[dict]:
    pass
