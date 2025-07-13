from typing import List, Dict, Any

def sort_key(sig: dict) -> tuple[str, int]:
    """Sort key function for signal lists.

    Sorts primarily by signal name, then by index (default 0 if missing).

    Args:
        sig: A signal dictionary, typically from the flatten stage.

    Returns:
        A tuple (name, index) for use in sorting.
    """
    return (sig["name"], sig.get("index", 0))

def normalize_dicts(lst: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalizes a list of signal dictionaries for comparison.

    This ensures consistent key ordering within each dictionary,
    so they can be reliably compared even if key insertion order varies.

    Args:
        lst: A list of signal dictionaries to normalize.

    Returns:
        A new list of dictionaries with sorted keys.
    """
    return [dict(sorted(d.items())) for d in lst]

def assert_flat_signals_equal(
        actual: List[Dict[str, Any]],
        expected: List[Dict[str, Any]]
) -> None:
    """
    Assert that two lists of flattened signals are equal, regardless of index

    """
    try:    
        sorted_actual = sorted(actual, key=lambda d: d['index'])
        sorted_expected = sorted(expected, key=lambda d: d['index'])
    except KeyError as e:
        raise ValueError(
                f"Missing 'index' key in signal entry during comparison: {e}"
        )
    assert sorted_actual == sorted_expected

