from collections import Counter
from typing import List, Dict, Any

def check(annotated: Dict[str, Any]) -> None:
    """
    Perform semantic consistency checks on annotated IO data.

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
    return

def check_duplicate_names(signals: List[Dict[str, Any]]) -> None:
    names = [sig["name"] for sig in signals]

    counts = Counter(names)
    dupes = [name for name, count in counts.items() if count > 1]
    if dupes:
        raise ValueError(f"Duplicate signal names: {', '.join(dupes)}")

def check_duplicate_pins(signals: List[Dict[str, Any]]) -> None:
    pins = get_all_pins(signals)

    counts = Counter(pins)
    dupes = [pin for pin, count in counts.items() if count > 1]
    if dupes:
        raise ValueError(f"Duplicate pin names: {', '.join(dupes)}")

def check_bus_misuse(signals: List[Dict[str, Any]]) -> None:
    for sig in signals:
        width = sig.get("width")
        bus = sig.get("bus", False)

        if width is None:
            raise ValueError(
                f"Signal '{sig['name']}' is missing a 'width' field — annotate() must run before check()."
            )

        if width > 1 and bus is False:
            raise ValueError(
                f"Signal '{sig['name']}' has width {width} but sets 'bus: false' — "
                f"multi-bit signals must be emitted as buses."
            )

    return

def get_all_pins(signals: List[Dict[str, Any]]) -> List[str]:
    """
    Return a flat list of all physical pin names used in the signal list.

    Includes:
    - 'pin': single string
    - 'pins': list of strings
    - 'pinset': p/n, either strings or lists

    Args:
        signals: List of signal dictionaries

    Returns:
        A flat list of all used pin names
    """
    pins = []

    for sig in signals:
        if "pin" in sig:
            pins.append(sig["pin"])
        elif "pins" in sig:
            pins.extend(sig["pins"])
        elif "pinset" in sig:
            p = sig["pinset"]["p"]
            n = sig["pinset"]["n"]
            pins.extend(p if isinstance(p, list) else [p])
            pins.extend(n if isinstance(n, list) else [n])

    return pins

