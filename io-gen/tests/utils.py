from typing import List, Dict, Any

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

