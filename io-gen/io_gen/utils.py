from typing import Any

def is_pins_scalar(signal: dict) -> bool:
    return 'pins' in signal and isinstance(signal['pins'], str)

def is_pins_array(signal: dict) -> bool:
    return 'pins' in signal and isinstance(signal['pins'], list)

def is_pinset_scalar(signal: dict) -> bool:
    """Return True if the signal is a scalar differential pair.

    Raises:
        ValueError: If p and n types mismatch or are unsupported.
    """
    if 'pinset' not in signal:
        return False

    pinset = signal['pinset']
    p_pins = pinset.get('p')
    n_pins = pinset.get('n')

    if type(p_pins) != type(n_pins):
        msg = (
            f"Signal '{signal.get('name', '?')}' has mismatched types in 'pinset': "
            f"'p' is {type(p_pins).__name__}, 'n' is {type(n_pins).__name__}. "
            f"Both must be strings for a scalar pair or lists of equal length."
        )
        raise ValueError(msg)

    if isinstance(p_pins, str):
        return True
    elif isinstance(p_pins, list):
        return False
    else:
        msg = (
            f"Signal '{signal.get('name', '?')}' has unsupported pinset types: "
            f"{type(p_pins).__name__}. Must be str or list."
        )
        raise ValueError(msg)

def is_pinset_array(signal: dict) -> bool:
    """Return True if the signal is a differential pinset array.

    Raises:
        ValueError: If p and n types mismatch or are unsupported.
    """
    if 'pinset' not in signal:
        return False

    pinset = signal['pinset']
    p_pins = pinset.get('p')
    n_pins = pinset.get('n')

    if type(p_pins) != type(n_pins):
        msg = (
            f"Signal '{signal.get('name', '?')}' has mismatched types in 'pinset': "
            f"'p' is {type(p_pins).__name__}, 'n' is {type(n_pins).__name__}. "
            f"Both must be lists of equal length or both must be strings."
        )
        raise ValueError(msg)

    if isinstance(p_pins, list):
        return True
    elif isinstance(p_pins, str):
        return False
    else:
        msg = (
            f"Signal '{signal.get('name', '?')}' has unsupported pinset types: "
            f"{type(p_pins).__name__}. Must be str or list."
        )
        raise ValueError(msg)

def is_multibank(signal: dict) -> bool:
    return 'multibank' in signal and isinstance(signal['multibank'], list)

def is_mixed_multibank(signal: dict) -> bool:
    """Returns true if a multibank has mixed pin and pinset fragments"""
    if not is_multibank(signal):
        msg = "Signal '{signal['name']}' is not a multibank signal"
        raise ValueError(msg)

    # Also need to expressly ban the mixture of single pin signals with
    # differential pairs. It isn't somethign that makes much sense
    fragment_types = []
    for fragment in signal['multibank']:
        if 'pins' in fragment:
            fragment_types.append('pins')
        elif 'pinset' in fragment:
            fragment_types.append('pinset')
        else:
            msg = f"Signal '{signal['name']}' contains unknown pin types"
            raise ValueError(msg)

    return len(set(fragment_types)) > 1

def is_single_ended_signal(pins: list[dict[str, Any]]) -> bool:
    """Determine if a signal is composed entirely of single-ended pins.

    Args:
        pins: The list of flattened pin entries for a single signal.

    Returns:
        True if all pins are single-ended (have 'pins' key),
        False if all pins are differential (have 'p' and 'n' keys).

    Raises:
        ValueError: If the pin types are mixed or malformed.

    """
    is_single = False
    is_diff = False

    for pin in pins:
        if 'pin' in pin:
            is_single = True
        elif 'p' in pin and 'n' in pin:
            is_diff = True
        else:
            msg = f"malformed pin entry: {pin}"
            raise ValueError(msg)

        if is_single and is_diff:
            msg = f"Mixed single-ended and differential pins in signal"
            raise ValueError(msg)

    return is_single

