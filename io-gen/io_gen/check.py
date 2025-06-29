def check(normalized: dict) -> None:
        """
    Perform semantic consistency checks on normalized IO data.

    This function validates internal correctness of the normalized input
    (as produced by `normalize()`), beyond what JSON Schema can express.

    Specifically, it checks for:

    - Duplicate signal names
    - Duplicate pin assignments (across `pin`, `pins`, and `pinset`)
    - Signals referencing undefined banks (should not happen post-normalize)
    - Pinset objects with mismatched array lengths for `p` and `n`
    - (Optional) Other design rule checks as needed for HDL generation

    Note:
        This function does not yet perform part-specific compatibilty checks.
        These may be added in the future, once the tool is extended to support
        part-specific resource descriptions (probably through a JSON description
        of what it is capable of).

    This function raises an error on the first violation encountered.

    Args:
        normalized (dict): Normalized IO definition, including keys:
            - "title": str
            - "part": str
            - "banks": dict[int, dict]
            - "signals": list[dict]

    Raises:
        ValueError: If semantic violations are found in the input data.

    """
