from typing import Any

# TODO: These should get pulled from JSON
ENUM_BANK_PERFORMANCE = {"HP", "HR", "HD"}


def validate_bank_table(bank_table: dict[int, dict[str, Any]]) -> None:
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
