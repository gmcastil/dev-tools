from typing import Dict, Any, List

def extract_signal_table(signals: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Extract the signal table from the input YAML signal list.

    This function builds a per-signal metadata table (width, group, comment, etc.)
    based on the signal entries in the YAML. It assumes the input has already
    passed schema validation.

    Args:
        signals: List of signal definitions from the YAML input.

    Returns:
        A dictionary keyed by signal name, where each value contains
        signal-level metadata.
    """
    pass


def validate_signal_table(signal_table: Dict[str, Dict[str, Any]]) -> None:
    """
    Validate the signal table for internal consistency.

    This includes checks for:
    - Duplicate signal names
    - Required metadata fields like width or group
    - Valid field types

    Args:
        signal_table: The extracted signal metadata table.

    Raises:
        ValueError: If any validation conditions are violated.
    """
    pass

