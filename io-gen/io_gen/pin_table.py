from typing import Dict, Any, List

def extract_pin_table(
    signals: List[Dict[str, Any]],
    bank_table: Dict[int, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Extract the flattened pin table from the full YAML input.

    This function transforms all signal fragments into a flat list of atomic
    pins or differential pairs. It combines information from signals,
    the signal table, and the bank table.

    Args:
        signals: Raw signal list from YAML.
        signal_table: The extracted per-signal metadata table.
        bank_table: The extracted per-bank metadata table.

    Returns:
        A list of dicts, one per atomic pin or pin pair, each with full metadata.
    """
    return []


def validate_pin_table(pin_table: List[Dict[str, Any]]) -> None:
    """
    Validate the flattened pin table for correctness.

    This includes checks like:
    - Unique (name, index) per signal
    - No reuse of package pins
    - Required metadata fields present

    Args:
        pin_table: The flat list of pins/pairs extracted from signals.

    Raises:
        ValueError: If the pin table violates structural or uniqueness constraints.
    """
    pass

