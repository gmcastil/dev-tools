from typing import Any

from io_gen.bank_table import get_bank_iostandard


def flatten_scalar_pins(
    signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Flattens a signal into a list of pins"""
    assert "pins" in signal, f"Signal '{signal['name']}' is not a single-ended signal"

    entry = get_pin_table_entry(signal)
    entry["index"] = 0
    entry["pin"] = signal["pins"]
    entry["iostandard"] = resolve_iostandard(signal, bank_table)
    pin_table_entries = [entry]

    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries


def flatten_array_pins(
    signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Flattens a signal into a list of pins"""
    assert "pins" in signal, f"Signal '{signal['name']}' is not an array of pins"

    pin_table_entries = []
    for index, pin in enumerate(signal["pins"]):
        entry = get_pin_table_entry(signal)
        entry["index"] = index
        entry["pin"] = pin
        entry["iostandard"] = resolve_iostandard(signal, bank_table)
        pin_table_entries.append(entry)
    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries


def flatten_scalar_pinset(
    signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Flattens a signal into a list of pin pairs"""
    assert signal["diff_pair"], f"Signal '{signal['name']}' is not a differential pair"

    entry = get_pin_table_entry(signal)
    entry["index"] = 0
    entry["p"] = signal["pinset"]["p"]
    entry["n"] = signal["pinset"]["n"]
    entry["iostandard"] = resolve_iostandard(signal, bank_table)
    pin_table_entries = [entry]

    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries


def flatten_array_pinset(
    signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Flattens a signal into a list of pin pairs"""
    assert signal["diff_pair"], f"Signal '{signal['name']}' is not a differential pair"

    pin_table_entries = []
    for index, (pin_p, pin_n) in enumerate(
        zip(signal["pinset"]["p"], signal["pinset"]["n"])
    ):
        entry = get_pin_table_entry(signal)
        entry["index"] = index
        entry["p"] = pin_p
        entry["n"] = pin_n
        entry["iostandard"] = resolve_iostandard(signal, bank_table)
        pin_table_entries.append(entry)

    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries


def flatten_multibank_pins(
    signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    name = signal["name"]

    assert "multibank" in signal, f"Signal '{name}' is not a multibank signal"
    assert not signal["diff_pair"], f"Signal '{name}' is not a differential signal"

    pin_table_entries = []

    # If we are inheriting the signal-level iostandard, we get it now
    signal_iostandard = signal.get("iostandard")

    for fragment in signal["multibank"]:
        # If a signal level iostandard was provided, we use it for every pin
        # otherwise, we use whatever the fragment provides (and every fragment has
        # to provide a bank)
        if signal_iostandard is None:
            iostandard = resolve_iostandard_multibank(fragment, bank_table)
        else:
            iostandard = signal_iostandard

        offset = fragment["offset"]
        pins = fragment["pins"]

        # Handle single pins first
        if isinstance(pins, str):
            entry = get_pin_table_entry(signal)
            entry["pin"] = pins
            entry["index"] = offset
            entry["iostandard"] = iostandard
            pin_table_entries.append(entry)

        # Now handle pin arrays
        else:
            for index, pin in enumerate(pins, offset):
                # The validation step will guarantee that both p and n elements are the same
                # type, but we still need to validate that the lengths are the same and account
                # for different types (list vs. strings)
                entry = get_pin_table_entry(signal)
                entry["pin"] = pin
                entry["index"] = index
                entry["iostandard"] = iostandard
                pin_table_entries.append(entry)

    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries


def flatten_multibank_pinset(
    signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    name = signal["name"]

    assert "multibank" in signal, f"Signal '{name}' is not a multibank signal"
    assert signal["diff_pair"], f"Signal '{name}' is not a differential signal"

    pin_table_entries = []

    # If we are inheriting the signal-level iostandard, we get it now
    signal_iostandard = signal.get("iostandard")

    for fragment in signal["multibank"]:
        # If a signal level iostandard was provided, we use it for every pin
        # otherwise, we use whatever the fragment provides (and every fragment has
        # to provide a bank)
        if signal_iostandard is None:
            iostandard = resolve_iostandard_multibank(fragment, bank_table)
        else:
            iostandard = signal_iostandard

        offset = fragment["offset"]
        pinset = fragment["pinset"]

        # Handle single pin pairs first
        if isinstance(pinset["p"], str) and isinstance(pinset["n"], str):
            entry = get_pin_table_entry(signal)
            entry["p"] = pinset["p"]
            entry["n"] = pinset["n"]
            entry["index"] = offset
            entry["iostandard"] = iostandard
            pin_table_entries.append(entry)
        else:
            for index, (p_pin, n_pin) in enumerate(
                zip(pinset["p"], pinset["n"]), offset
            ):
                entry = get_pin_table_entry(signal)
                entry["p"] = p_pin
                entry["n"] = n_pin
                entry["index"] = index
                entry["iostandard"] = iostandard
                pin_table_entries.append(entry)

    check_flattened_width(signal, pin_table_entries)

    return pin_table_entries


def resolve_iostandard(
    signal: dict[str, Any], bank_table: dict[int, dict[str, Any]]
) -> str:
    """Resolves the iostandard for a signal via inheritance or direct specification"""
    name = signal["name"]

    # Try to set iostandard explicitly
    iostandard = signal.get("iostandard")
    if iostandard is None:
        # Try to get it from the bank table - this should be there if we're validated
        bank: int = signal["bank"]
        iostandard = get_bank_iostandard(bank, bank_table)
        if iostandard is None:
            msg = f"Cannot set 'iostandard' for signal '{name}'"
            raise ValueError(msg)
        else:
            return iostandard
    else:
        return iostandard


def resolve_iostandard_multibank(
    fragment: dict[str, Any], bank_table: dict[int, dict[str, Any]]
) -> str:
    """Resolves the iostandard for a bank fragment via inheritance or direct specification"""

    # Is it defined explicitly?
    if "iostandard" not in fragment:
        # No, so try to inherit from the bank
        bank = fragment["bank"]
        iostandard = get_bank_iostandard(bank, bank_table)
    # This fragment specifies its iostandard explicitly
    else:
        iostandard = fragment["iostandard"]

    return iostandard


def check_flattened_width(
    signal: dict[str, Any], pin_entries: list[dict[str, Any]]
) -> None:
    """Checks that flattened pin entries have the appropriate width and range"""

    actual_indices = sorted(entry["index"] for entry in pin_entries)
    expected_indices = list(range(0, signal["width"]))

    if actual_indices != expected_indices:
        msg = (
            f"Signal '{signal['name']}' has index or width mismatch: "
            f"expected {expected_indices}, but got {actual_indices}"
        )
        raise ValueError(msg)


def get_pin_table_entry(signal: dict[str, Any]) -> dict[str, Any]:
    """Returns a minimal pin table entry with name, direction, buffer, and iostandard

    Args:
        signal - Entry from the signal table to use as a starting point for a pin table entry
        bank_table - Bank table

    Returns:
        dict

    """
    # Every entry in the pin table will get these values directly fro the signal its a part of
    entry = {
        "name": signal["name"],
        "direction": signal["direction"],
        "buffer": signal["buffer"],
        "diff_pair": signal["diff_pair"],
        "bus": signal["bus"],
    }

    return entry
