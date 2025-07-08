from typing import Dict, Any

# These should get pulled from JSON
ENUM_BANK_PERFORMANCE = {"HP", "HR", "HD"}

def extract_bank_table(banks: Dict[str, Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """Convert string-keyed YAML bank dict to int-keyed bank table with validated entries."""

def extract_bank_table(banks: Dict[int, Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """
    Extract and normalize the bank table from raw YAML input.

    This function simply returns the `banks` dictionary as-is, assuming
    that all entries have already been schema-validated and are keyed by
    integer bank numbers.

    Args:
        banks: Dictionary of bank definitions from YAML. Keys must be integers.

    Returns:
        A dictionary representing the internal bank table, where each key is a
        bank number and each value is a dict of attributes like `iostandard` and `performance`.
    """
    return banks

def validate_bank_table(bank_table: Dict[int, Dict[str, Any]]) -> None:
    """
    Validate the extracted bank table for correctness.

    This includes checking that required fields are present (`iostandard`, `performance`)
    and that the performance type is valid.

    Args:
        bank_table: The extracted bank table.

    Raises:
        ValueError: If required fields are missing or invalid values are used.
    """
    for bank_num, entry in bank_table.items():
        if "iostandard" not in entry:
            raise ValueError(f"Bank {bank_num} is missing required key 'iostandard'")
        if "performance" not in entry:
            raise ValueError(f"Bank {bank_num} is missing required key 'performance'")
        if entry["performance"] not in ENUM_BANK_PERFORMANCE:
            raise ValueError(
                f"Bank {bank_num} has invalid performance type: {entry['performance']}"
            )

