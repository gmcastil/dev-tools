from copy import deepcopy
from typing import List, Dict, Any

def flatten_signals(signals: List[Dict], banks: Dict[int, Dict]) -> List[Dict]:
    """
    Flatten the list of signals, resolving inheritance from bank definitions.

    Each returned signal dict includes all explicitly provided keys,
    plus inherited 'iostandard' if not overridden.

    Args:
        signals (list): List of signal dictionaries from validated YAML.
        banks (dict): Flattened bank lookup table (bank number -> bank attributes).

    Returns:
        List[dict]: Flat list of resolved signal dictionaries.

    Raises:
        ValueError: If a signal references a bank number not present in the bank list.

    """
    flat = []

    for signal in signals:
        if "pin" in signal:
            flat.extend(flatten_pin(signal, banks))
        elif "pins" in signal:
            flat.extend(flatten_pins(signal, banks))
        elif "pinset" in signal:
            flat.extend(flatten_pinset(signal, banks))
        elif "multibank" in signal:
            flat.extend(flatten_multibank(signal, banks))
        else:
            msg = f"Signal '{signal['name']}' has no valid pin definition"
            raise ValueError(msg)
    
    return flat

def flatten_pin(signal: dict, banks: Dict[int, dict]) -> list[dict]:
    # Going to mangle this and return it, so copy now
    signal_c = deepcopy(signal)

    if 'pin' not in signal_c:
        msg = f"Signal '{signal_c['name']}' has a missing pin value"
        raise ValueError(msg)

    if 'direction' not in signal_c:
        msg = f"Signal '{signal_c['name']}' has a missing direction"
        raise ValueError(msg)

    # Set 'as_bus' even if not included
    signal_c['as_bus'] = signal_c.get('as_bus', False)

    # Check if the signal itself has the IO standard defined
    if "iostandard" not in signal_c:
        bank = signal_c.get("bank", None)
        if bank is not None and bank in banks:
            signal_c['iostandard'] = banks[bank]['iostandard']
        else:
            msg = f"Signal '{signal_c['name']}' has no bank or IOSTANDARD defined"
            raise ValueError(msg)

    # The index for a single pin is always 0
    signal_c['index'] = 0

    return [signal_c]

def flatten_pins(signal: dict, banks: dict[int, dict]) -> list[dict]:

    flattened = []
    signal_c = deepcopy(signal)

    # Will be iterating over the pins, so need to move this list out of the copy
    # before mutating and flattening
    pins = signal_c.pop('pins', None)
    if pins is None:
        msg = f"Signal '{signal_c['name']}' has no pins defined"
        raise ValueError(msg)

    if 'direction' not in signal_c:
        msg = f"Signal '{signal_c['name']}' has a missing direction"
        raise ValueError(msg)

    # Set 'as_bus' to false, even if it was included
    signal_c['as_bus'] = False

    # Now set the iostandard, which may or may not be inherited from the bank
    if 'iostandard' not in signal_c:
        bank = signal_c.get("bank", None)
        if bank is not None and bank in banks:
            signal_c['iostandard'] = banks[bank]['iostandard']
        else:
            msg = f"Signal '{signal_c['name']}' has no bank or IOSTANDARD defined"
            raise ValueError(msg)

    # Safe to iterate over pins, because they came from the copy
    for index, pin in enumerate(pins):
        signal_cc = deepcopy(signal_c)

        signal_cc['index'] = index
        signal_cc['pin'] = pin

        flattened.append(signal_cc)

    return flattened

def flatten_pinset(signal: dict, banks: dict[int, dict]) -> list[dict]:

    flattened = []
    signal_c = deepcopy(signal)

    # Before doing anything verify that the shapes are correct
    pinset = signal_c.pop('pinset', None)
    if pinset is None:
        msg = f"Signal '{signal_c['name']}' has no pinset defined"
        raise ValueError(msg)

    if 'direction' not in signal_c:
        msg = f"Signal '{signal_c['name']}' has a missing direction"
        raise ValueError(msg)

    if 'iostandard' not in signal_c:
        bank = signal_c.get("bank", None)
        if bank is not None and bank in banks:
            signal_c['iostandard'] = banks[bank]['iostandard']
        else:
            msg = f"Signal '{signal_c['name']}' has no bank or IOSTANDARD defined"
            raise ValueError(msg)

    # Now make sure that the types are the same - this is guaranteed,
    # because we checked earlier for pinset to exist as a key
    if type(pinset['p']) != type(pinset['n']):
        msg = (
                f"Signal '{signal['name']}' has mismatched pinset types: "
                f"'p' is type {type(pinset['p']).__name__}, "
                f"'n' is type {type(pinset['n']).__name__}"
                )
        raise ValueError(msg)

    if isinstance(pinset['p'], str):
        # Flatten the pinset pair to two p and n signals
        signal_c['p'] = pinset['p']
        signal_c['n'] = pinset['n']
        # Set the 'as_bus' value
        signal_c['as_bus'] = signal_c.get('as_bus', False)
        # A single pinset has an index of 1
        signal_c['index'] = 0
        flattened.append(signal_c)

    elif isinstance(pinset['p'], list):
        # The schema cannot guarantee taht these two pinsets are the smae length so
        # it has to be checked here and raised on
        p_pins = pinset['p']
        n_pins = pinset['n']
        # The 'as_bus' value has to be false here
        signal_c['as_bus'] = False
        if len(p_pins) != len(n_pins):
            msg = (
                    f"Signal '{signal['name']}' has mismatched differential pinset lengths: "
                    f"'p' has {len(p_pins)} elements, 'n' has {len(n_pins)} elements"
                    )
            raise ValueError(msg)

        # Now we can flatten the list of pins
        for index, (p_pin, n_pin) in enumerate(zip(p_pins, n_pins)):
            signal_cc = deepcopy(signal_c)
            # Flatten the pinset pair to two p and n signals
            signal_cc['p'] = p_pin
            signal_cc['n'] = n_pin
            signal_cc['index'] = index
            flattened.append(signal_cc)

    else:
        msg = (
                f"Signal '{signal['name']}' has invalid pinset types: "
                f"'p' is type {type(pinset['p']).__name__}, "
                f"'n' is type {type(pinset['n']).__name__}; "
                f"both must be str or list"
                )
        raise ValueError(msg)

    return flattened

def flatten_multibank(signal: dict, banks: dict[int, dict]) -> list[dict]:
    flattened = []
    signal_c = deepcopy(signal)

    width = signal_c.get('width', None)
    if width is None:
        msg = f"Signal '{signal_c['name']}' has a missing width"
        raise ValueError(msg)

    if 'direction' not in signal_c:
        msg = f"Signal '{signal_c['name']}' has a missing direction"
        raise ValueError(msg)

    # Before doing anything verify that the shapes are correct
    multibank = signal_c.pop('multibank', None)
    if multibank is None:
        msg = f"Signal '{signal_c['name']}' has no multibank defined"
        raise ValueError(msg)

    # Handle the single-bit scalar 'as_bus' flag before processing fragments. The
    # problematic case is when a multibank signal includes a scalar 'pin' or
    # 'pinset' fragment and the top-level signal has 'as_bus = true' . These
    # scalar fragments are part of a wider bus, so treating them as standalone
    # 1-bit buses (as 'as_bus': true' would imply) is invalid. Since the
    # flatten_* functions operate on fragments without awareness of the larger
    # multibank context, we must prevent incorrect propagation of 'as_bus: true'
    # here. This isn't an entirely far-fetched idea - the schema can't catch
    # illegal use of the 'as_bus' property because it depends on the lengths and
    # types of the other signals involved.
    if len(multibank) == 1 and ('pin' in multibank[0] or 'pinset' in multibank[0]):
        as_bus = signal_c.get('as_bus', False)
    else:
        as_bus = False

    # We already know how to flatten pin, pins, and pinsets, if they look right
    for fragment in multibank:
        # So, we make a copy of just the fragment (so, just a bank of pins)
        fragment_c = deepcopy(fragment)

        # Add fields required for signals before dispatching to the
        # flattener functions
        fragment_c['name'] = signal_c['name']
        fragment_c['direction'] = signal_c['direction']
        fragment_c['buffer'] = signal_c['buffer']

        # Handling IOSTANDARD is special because we inherit per bank OR defined
        # for the entire signal
        iostandard = signal_c.get('iostandard', None)
        # Now we check to see if iostandard was defined for the top
        # level signal and if it was, we make it the default - that
        # means that the flatten functions will get called with the
        # banks argument, but then not need it.
        if iostandard is not None:
            fragment_c['iostandard'] = iostandard

        # Now we insert the bus value we extracted from the top level
        # signal into the signal fragment, before calling the appropriate
        # flattener
        fragment_c['as_bus'] = as_bus
        if 'pin' in fragment:
            flat_fragment = flatten_pin(fragment_c, banks)
        elif 'pins' in fragment:
            flat_fragment = flatten_pins(fragment_c, banks)
        elif 'pinset' in fragment:
            flat_fragment = flatten_pinset(fragment_c, banks)
        else:
            msg = f"Signal '{signal['name']}' has no valid pin definition"
            raise ValueError(msg)

        # Now we need to create the index for each pin in the flattened fragment
        # based on the offset (iterating over list of pins of flattened fragment
        # of a multibank entry)
        try:
            offset = fragment_c["offset"]  # This should always exist, per schema
            for index, pin in enumerate(flat_fragment, offset):
                pin["index"] = index
                flattened.append(pin)
        except KeyError:
            msg = (
                f"Internal error: expected 'offset' key missing from fragment_c during index assignment.\n"
                f"This likely indicates an inconsistency in the multibank signal model.\n"
                f"Fragment entry: {fragment_c.get('name', '<unknown>')}"
            )
            raise ValueError(msg)

    # Now remove the internal keys that were added along the way - these
    # should absolutely all exist and if they don't, it's likely a bug in the
    # multibank handling
    for pin in flattened:
        try:
            del pin["offset"]
        except KeyError:
            msg = (
                f"Internal error: expected internal key 'offset' not found in flattened signal.\n"
                f"This likely indicates a bug in multibank flattening or an earlier mutation step.\n"
                f"Signal entry: {pin.get('name', '<unknown>')}"
            )
            raise ValueError(msg)

    flattened_indices = [entry["index"] for entry in flattened]
    if sorted(flattened_indices) != list(range(width)):
        raise ValueError(
            f"Signal '{signal['name']}' has invalid index mapping. "
            f"Expected contiguous 0..{width-1}, got: {sorted(flattened_indices)}. "
            "Check offset, pin counts, and declared width."
        )

    return flattened

def flatten_banks(banks: list[dict]) -> dict[int, dict]:
    """
    Flatten a list of bank entries into a lookup dictionary by bank number.

    Each bank must include 'bank', 'iostandard', and 'performance'.
    An optional 'comment' field will be preserved if present.

    Duplicate bank numbers will raise a ValueError.

    Args:
        banks (list): List of bank dictionaries from validated YAML.

    Returns:
        dict[int, dict]: Mapping of bank number to bank attributes.
                         Each value includes at least 'iostandard' and 'performance',
                         and optionally 'comment' if present.

    Raises:
        ValueError: If duplicate bank numbers are detected.

    """
    result = {}

    for bank in banks:
        bank_copy = deepcopy(bank)  # Copy because we're going to mutate the bank dict
        number = bank_copy["bank"]
        # Recall that the keys in the result dict are the bank numbers,
        # so we check for duplicates
        if number in result:
            raise ValueError(f"Found duplicate bank {number} entry")

        # Flattened bank structure is just going to have the bank number
        # removed and used as the key in the result
        del bank_copy["bank"]
        result[number] = bank_copy

    return result

