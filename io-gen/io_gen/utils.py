from typing import Any

def is_scalar_pins(signal: dict[str, Any]) -> bool:
    """Returns true if signal from YAML is a single ended pin"""
    if 'pins' not in signal:
        return False

    # Don't do any width checks - that's later
    if isinstance(signal['pins'], str):
        return True
    else:
        return False

def is_scalar_pinset(signal: dict[str, Any]) -> bool:
    """Returns true if signal from YAML is a single diff pair"""
    if 'pinset' not in signal:
        return False

    pinset = signal['pinset']
    p_pins = pinset.get('p')
    n_pins = pinset.get('n')

    if type(p_pins) != type(n_pins):
        msg = (
            f"Signal '{signal['name']}' has mismatched types in 'pinset': "
            f"'p' is {type(p_pins).__name__}, 'n' is {type(n_pins).__name__}. "
            f"Both must be lists of equal length or both must be strings."
        )
        raise ValueError(msg)

    # Don't do any width checks - that's later
    if isinstance(p_pins, list):
        return False
    elif isinstance(p_pins, str):
        return True
    else:
        msg = (
            f"Signal '{signal.get('name', '?')}' has unsupported pinset types: "
            f"{type(p_pins).__name__}. Must be str or list."
        )
        raise ValueError(msg)

def is_array_pins(signal: dict) -> bool:
    """Returns true if signal from YAML is an array of single-ended pins"""
    if 'pins' not in signal:
        return False

    if isinstance(signal['pins'], str):
        return False
    else:
        return True

def is_array_pinset(signal: dict[str, Any]) -> bool:
    """Returns true if signal from YAML is an array of diff pairs"""
    if 'pinset' not in signal:
        return False

    pinset = signal['pinset']
    p_pins = pinset.get('p')
    n_pins = pinset.get('n')

    if type(p_pins) != type(n_pins):
        msg = (
            f"Signal '{signal['name']}' has mismatched types in 'pinset': "
            f"'p' is {type(p_pins).__name__}, 'n' is {type(n_pins).__name__}. "
            f"Both must be lists of equal length or both must be strings."
        )
        raise ValueError(msg)

    # Don't do any width checks - that's later
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

def is_multibank_pins(signal: dict[str, Any]) -> bool:
    """Returns true if signal from YAML is multibank array of single ended pins"""
    if 'multibank' not in signal:
        return False

    if not signal['multibank']:
        msg = f"Multibank signal '{signal['name']}' has a missing pin definition"
        raise ValueError(msg)

    if is_mixed_multibank(signal):
        msg = f"Multibank signal {signal['name']} contains mixed pin definitions"
        raise ValueError(msg)

    if 'pins' in signal['multibank'][0]:
        return True
    else:
        return False
     
def is_multibank_pinset(signal: dict[str, Any]) -> bool:
    """Returns true if signal from YAML is multibank array of diff pairs"""
    if 'multibank' not in signal:
        return False

    if not signal['multibank']:
        msg = f"Multibank signal '{signal['name']}' has a missing pin definition"
        raise ValueError(msg)

    if is_mixed_multibank(signal):
        msg = f"Multibank signal {signal['name']} contains mixed pin definitions"
        raise ValueError(msg)

    if 'pinset' in signal['multibank'][0]:
        return True
    else:
        return False

def is_mixed_multibank(signal: dict[str, Any]) -> bool:
    """Returns true if a multibank signal has mixed pin and pinset fragments"""
    assert 'multibank' in signal, f"Signal '{signal['name']}' does not contain 'multibank'"

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

def check_multibank_width(signal: dict[str, Any]) -> None:
    """Check that multibank signals define their offsets and widths correctly

    Raises:
        ValueError: If indices are missing, overlapping, or misaligned with declared width.
    """
    assert 'multibank' in signal, f"Signal '{signal['name']}' does not contain 'multibank'"

    width = signal["width"]
    expected = set(range(width))
    seen = set()

    for fragment in signal["multibank"]:
        count = get_multibank_fragment_width(fragment)

        offset = fragment["offset"]
        indices = set(range(offset, offset + count))
        overlap = seen & indices
        if overlap:
            msg = f"Overlapping multibank indices at offsets {sorted(overlap)}"
            raise ValueError(msg)

        seen.update(indices)

    if seen != expected:
        msg = (
            f"Multibank fragments cover indices {sorted(seen)}, "
            f"but expected full range 0..{width - 1}"
        )
        raise ValueError(msg)

def get_sig_width(signal: dict[str, Any]) -> int:
    """Returns width of a signal"""

    # Independently calculate the width of the signal - note that scalars do not need
    # to provide width, but if they do, we check it and error out if it isn't 1.
    if is_scalar_pins(signal) or is_scalar_pinset(signal):
        if signal.get('width', 1) > 1:
            msg = f"Scalar signal '{signal['name']}' has width > 1"
            raise ValueError(msg)
        else:
            return 1

    # Now we check the rest of the pin types and require that width is explicitly declared
    if signal.get("width") is None:
        msg = f"Signal '{signal['name']}' must declare 'width'"
        raise ValueError(msg)

    if is_array_pins(signal):
        width = len(signal['pins'])

    elif is_array_pinset(signal):
        pinset = signal['pinset']
        p_pins = pinset['p']
        n_pins = pinset['n']

        # Verify that the P and N sides are the same length
        if len(n_pins) != len(p_pins):
            msg = (
                f"Signal '{signal['name']}' has mismatched differential pair lengths: "
                f"{len(p_pins)} P-side pins vs {len(n_pins)} N-side pins"
                )
            raise ValueError(msg)

        width = len(p_pins)

    elif is_multibank_pins(signal) or is_multibank_pinset(signal):
        check_multibank_width(signal)
        width = sum(get_multibank_fragment_width(fragment) for fragment in signal['multibank'])

    else:
        msg = f"Signal '{signal['name']}' contains unknown pin types"
        raise ValueError(msg)

    if signal['width'] != width:
        msg = (
            f"Signal '{signal['name']}' has declared width {signal.get('width')}, "
            f"but actual width is {width}"
        )
        raise ValueError(msg)

    return width

def get_multibank_fragment_width(fragment: dict) -> int:
    """Returns the length of a fragment from a multibank signal"""
    if "pins" in fragment:
        pins = fragment['pins']
        count = 1 if isinstance(pins, str) else len(pins)
    elif "pinset" in fragment:
        pinset_p = fragment['pinset']['p']
        count = 1 if isinstance(pinset_p, str) else len(pinset_p)
    else:
        msg = f"Malformed multibank fragment: missing 'pins' or 'pinset'"
        raise ValueError(msg)

    return count

