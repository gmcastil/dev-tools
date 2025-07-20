from typing import Any


def extract_bank_table(banks: dict[int, dict[str, Any]]) -> dict[int, dict[str, Any]]:
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


def get_bank_iostandard(number: int, bank_table: dict[int, dict[str, Any]]) -> str:
    """Looks up the 'iostandard' property for a bank from the bank table"""

    if number not in bank_table:
        msg = f"Bank table does not contain an entry for bank {number}"
        raise ValueError(msg)

    # The bank 'iostandard' key is required by the schema
    assert (
        "iostandard" in bank_table[number]
    ), "Bank 'iostandard' is missing from bank table entry"

    iostandard = bank_table[number]["iostandard"]
    return iostandard


