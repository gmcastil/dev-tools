import logging

logger = logging.getLogger(__name__)

from typing import Any

from io_gen.utils import (
    is_array_pins,
    is_array_pinset,
    is_multibank_pins,
    is_multibank_pinset,
    is_scalar_pins,
    is_scalar_pinset,
)


def validate_signal_table(signal_table: list[dict[str, Any]]) -> None:
    """
    Validate the signal table for semantic correctness before flattening.

    This checks each signal for valid structure and intent, ensuring that fields
    like 'bank' and 'iostandard' are used consistently and appropriately based
    on the signal's type.

    Args:
        signal_table: A list of structured signal dictionaries (pre-flattening).

    Raises:
        ValueError: If any signal entry is semantically invalid or ambiguous.

    """
    logger.debug("Validating signal table")
    for signal in signal_table:
        if is_scalar_pins(signal):
            validate_scalar_pins(signal)
        elif is_array_pins(signal):
            validate_array_pins(signal)
        elif is_scalar_pinset(signal):
            validate_scalar_pinset(signal)
        elif is_array_pinset(signal):
            validate_array_pinset(signal)
        elif is_multibank_pins(signal):
            validate_multibank_pins(signal)
        elif is_multibank_pinset(signal):
            validate_multibank_pinset(signal)
        else:
            msg = (
                f"Signal '{signal['name']}' has unrecognized or unsupported structure."
            )
            raise ValueError(msg)


def validate_scalar_pins(signal: dict[str, Any]) -> None:
    """Validate a single-ended scalar pin signal."""
    name = signal["name"]
    assert "pins" in signal, f"Signal '{name}' does not contain a 'pins' element"

    validate_required_fields(signal)
    validate_iostandard_bank_no_multibank(signal)

    # Width is allowed, but it has to be 1 or its an error
    width = signal.get("width", 1)
    if width != 1:
        msg = f"Signal '{name}' is scalar but defines invalid width={signal['width']}"
        raise ValueError(msg)

    # Last, we check the type to make sure its consistent
    if not isinstance(signal["pins"], str):
        msg = f"Signal '{name}' is not a scalar"
        raise ValueError(msg)


def validate_array_pins(signal: dict[str, Any]) -> None:
    """Validate a single-ended pin array signal.

    Ensures consistent use of 'bank' or 'iostandard', and verifies that pin arrays
    are declared with valid structure and field combinations.
    """

    name = signal["name"]
    assert "pins" in signal, f"Signal '{name}' does not contain a 'pins' element"

    validate_required_fields(signal)
    validate_iostandard_bank_no_multibank(signal)

    width = signal.get("width")
    if width is None:
        msg = f"Signal '{name}' is an array but does not define a width"
        raise ValueError(msg)

    # Last, we check the type to make sure its consistent
    if not isinstance(signal["pins"], list):
        msg = f"Signal '{name}' is not an array"
        raise ValueError(msg)


def validate_scalar_pinset(signal: dict[str, Any]) -> None:
    """Validate a scalar differential signal using 'pinset'.

    Confirms that the signal contains either a top-level 'iostandard' or inherits from a
    valid bank, and uses no conflicting fields.

    """
    name = signal["name"]
    assert "pinset" in signal, f"Signal '{name}' does not contain a 'pinset' element"

    validate_required_fields(signal)
    validate_iostandard_bank_no_multibank(signal)

    # Check that diff pairs are both present
    pinset = signal["pinset"]
    if not all(k in pinset for k in ("p", "n")):
        msg = f"Signal '{name}' is missing 'p' or 'n' keys in 'pinset'"
        raise ValueError

    # Check that both are strings (not lists)
    if not isinstance(pinset["p"], str) or not isinstance(pinset["n"], str):
        msg = f"Signal '{name}' has non-scalar types in 'pinset'"
        raise ValueError(msg)

    # Width is allowed, but it has to be 1 or its an error
    width = signal.get("width", 1)
    if width != 1:
        msg = f"Signal '{name}' is scalar but defines width={width}"
        raise ValueError(msg)


def validate_array_pinset(signal: dict[str, Any]) -> None:
    """Validate an array of differential signals using 'pinset'.

    Checks that each entry has appropriate structure and that either
    'bank' or 'iostandard' is declared for inheritance.
    """
    name = signal["name"]
    assert "pinset" in signal, f"Signal '{name}' does not contain a 'pinset' element"

    validate_required_fields(signal)
    validate_iostandard_bank_no_multibank(signal)

    # Check that diff pairs are both present
    pinset = signal["pinset"]
    if not all(k in pinset for k in ("p", "n")):
        msg = f"Signal '{name}' is missing 'p' or 'n' keys in 'pinset'"
        raise ValueError(msg)

    width = signal.get("width")
    if width is None:
        msg = f"Signal '{name}' is an array but does not define a width"
        raise ValueError(msg)

    # Check that both are lists of equal length
    if not isinstance(pinset["p"], list) or not isinstance(pinset["n"], list):
        msg = f"Signal '{name}' must have lists for both 'p' and 'n'"
        raise ValueError(msg)

    if len(pinset["p"]) != len(pinset["n"]) or len(pinset["p"]) != width:
        msg = (
            f"Signal '{name}' has mismatched pin pair lengths: "
            f"p={len(pinset['p'])}, n={len(pinset['n'])}, width={width}"
        )
        raise ValueError(msg)


def validate_multibank_pins(signal: dict[str, Any]) -> None:
    """Validate a multibank signal composed of single-ended pin fragments.

    Enforces correct use of 'iostandard' and 'bank' at the top and fragment levels,
    ensuring no invalid combinations are present.
    """
    name = signal["name"]
    assert (
        "multibank" in signal
    ), f"Signal '{name}' does not contain a 'multibank' element"

    validate_required_multibank_fields(signal)
    validate_iostandard_bank_yes_multibank(signal)

    multibank = signal["multibank"]
    for fragment in multibank:
        if not "pins" in fragment:
            msg = f"Signal '{name}' has mixed pin and pinset types"
            raise ValueError(msg)
        if not "offset" in fragment:
            msg = f"Signal '{name}' is missing required 'offset' field"
            raise ValueError(msg)
        if not "bank" in fragment:
            msg = f"Signal '{name}' is missing required 'bank' field in multibank fragment"
            raise ValueError(msg)


def validate_multibank_pinset(signal: dict[str, Any]) -> None:
    """Validate a multibank differential signal composed of pinset fragments.

    Ensures exclusive or consistent use of 'iostandard' across fragments and
    proper inheritance behavior from banks if not specified.
    """
    name = signal["name"]
    assert (
        "multibank" in signal
    ), f"Signal '{name}' does not contain a 'multibank' element"

    validate_required_multibank_fields(signal)
    validate_iostandard_bank_yes_multibank(signal)

    multibank = signal["multibank"]
    for fragment in multibank:
        if not "pinset" in fragment:
            msg = f"Signal '{name}' has mixed pin and pinset types"
            raise ValueError(msg)
        if not "offset" in fragment:
            msg = f"Signal '{name}' is missing required 'offset' field"
            raise ValueError(msg)
        if not "bank" in fragment:
            msg = f"Signal '{name}' is missing required 'bank' field in multibank fragment"
            raise ValueError(msg)


def validate_required_fields(signal: dict[str, Any]) -> None:
    """Validate that default and required fields are present"""

    # Required by schema
    name = signal["name"]

    if signal.get("direction", None) is None:
        msg = f"Signal '{name}' is missing required 'direction' field"
        raise ValueError(msg)

    if signal.get("buffer", None) is None:
        msg = f"Signal '{name}' is missing required 'buffer' field"
        raise ValueError(msg)

    if signal.get("diff_pair", None) is None:
        msg = f"Signal '{name}' is missing required 'diff_pair' field"
        raise ValueError(msg)

    if signal.get("bus", None) is None:
        msg = f"Signal '{name}' is missing required 'bus' field"
        raise ValueError(msg)

    # Groups is optional
    if "group" in signal:
        if not isinstance(signal["group"], str):
            msg = f"Signal '{name}' has optional 'group' field but of the wrong type"
            raise ValueError(msg)

    # Comment is optional, but structured
    if "comment" in signal:
        comment = signal["comment"]
        if not isinstance(comment, dict):
            msg = f"Signal '{name}' has optional 'comment' field but of the wrong type"
            raise ValueError(msg)
        extra_keys = set(comment.keys()) - {"xdc", "hdl"}
        if extra_keys:
            raise ValueError(f"Invalid keys in comment: {extra_keys}")


def validate_required_multibank_fields(signal: dict[str, Any]) -> None:
    """Validate that required fields for multibank signals are present"""
    name = signal["name"]
    assert (
        "multibank" in signal
    ), f"Signal '{name}' does not contain a 'multibank' element"

    # Make sure they didn't pass us an empty list
    multibank = signal["multibank"]
    if not multibank:
        msg = f"Signal '{name}' cannot define an empty multibank section"
        raise ValueError(msg)

    # Multibank signals are required to specify the bank in the multibank section
    if signal.get("bank"):
        msg = f"Signal '{name}' is a multibank signal but defines 'bank' in the signal"
        raise ValueError(msg)
    if signal.get("width") is None:
        msg = f"Signal '{name}' is missing required 'width' field"
        raise ValueError(msg)

    # Now validate all the other fields that every signal requires
    validate_required_fields(signal)


def validate_iostandard_bank_no_multibank(signal: dict[str, Any]) -> None:
    """Validate that iostandard or banks are present

    Pin and pinset arrays and scalars inherit their iostandard properties
    in the same way, so we validate them the same (either, or both with a note
    that we will check later during flattening, but not neither).

    Multibank validation is done differently.

    """
    name = signal["name"]
    assert (
        "multibank" in signal
    ), f"Signal '{name}' does not contain a 'multibank' element"

    if "iostandard" in signal and "bank" in signal:
        msg = (
            f"Signal '{name}' specifies both 'iostandard' and 'bank'; "
            f"consistency will be verified during flattening."
        )
        logger.info(msg)
    elif "iostandard" not in signal and "bank" not in signal:
        msg = f"Signal '{name}' must specify either 'iostandard' or 'bank'."
        raise ValueError(msg)


def validate_iostandard_bank_yes_multibank(signal: dict[str, Any]) -> None:
    """Validate that iostandard or banks are present for multibank signals

    Multibank signals inherit their iostandard properties differently than
    other signals, so we validate them here differently.

    """
    name = signal["name"]
    assert (
        "multibank" in signal
    ), f"Signal '{name}' does not contain a 'multibank' element"

    multibank = signal["multibank"]
    if not multibank:
        msg = f"Signal '{name}' cannot define an empty multibank section"
        raise ValueError(msg)

    # Multibank can inherit iostandard from the top level, in which case there
    # can be no iostandard in the fragments. If we do not inherit from the top level, then
    # we will either explicitly define the iostandard per bank, or inherit from the bank
    # number (recall that bank is a required key per the schema).
    if "iostandard" in signal:
        if any("iostandard" in fragment for fragment in multibank):
            msg = f"Signal '{name}' tries to override multibank 'iostandard'"
            raise ValueError(msg)
