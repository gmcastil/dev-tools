from io_gen.utils import is_single_ended_signal

from typing import Any

def emit_signal_xdc(signal: dict[str, Any], pins: list[dict[str, Any]]) -> list[str]:
    """Emit XDC constraints for a single logical signal.

    This function generates all `set_property` lines for one signal,
    based on its definition and corresponding flattened pin entries.

    Args:
        signal: The original signal definition from the signal table.
        pins: A list of flattened pin entries associated with this signal.

    Returns:
        A string containing XDC lines for this signal, separated by newlines.

    """
    is_single_ended = is_single_ended_signal(pins)

    # Sanity check here in case of improper filtering upstream
    assert all(pin['name'] == pins[0]['name'] for pin in pins)

    # Initialize the XDC block that is going to come from this signal with
    # whatever comments were supplied
    # TODO: This needs to wait until the schema is updated to include an XDC and HDL comment
    xdc_lines = []

    # Not all single bit signals actually get emitted that way - some are treated as
    # single bit buses for emission purposes
    if emit_as_single_bit_signal(signal, pins):
        pin = pins[0]
        name = pin['name']
        iostandard = pin['iostandard']

        if is_single_ended:
            port_name = f"{name}_pad"
            port = pin['pin']
            xdc_lines.extend(emit_single_ended_xdc(port_name, port, iostandard))
        else:
            p_name = f"{name}_p"
            n_name = f"{name}_n"
            p_port = pin['p']
            n_port = pin['n']
            xdc_lines.extend(emit_diff_pair_xdc(p_name, n_name, p_port, n_port, iostandard))

    else:
        xdc_lines = []
        for pin in pins:
            name = pin['name']

            # Recall that IOSTANDARD can vary across a signal if the signal is split
            # across multiple banks
            iostandard = pin['iostandard']

            if is_single_ended:
                port_name = f"{name}_pad"
                port = pin['pin']
                xdc_lines.extend(emit_single_ended_xdc(port_name, port, iostandard))
            else:
                p_name = f"{name}_p"
                n_name = f"{name}_n"
                p_port = pin['p']
                n_port = pin['n']
                xdc_lines.extend(emit_diff_pair_xdc(p_name, n_name, p_port, n_port, iostandard))

    return xdc_lines

def emit_single_ended_xdc(name: str, port: str, iostandard: str) -> list[str]:
    return [
            f"set_property PACKAGE_PIN {port} [get_ports {{{name}}}]",
            f"set_property IOSTANDARD {iostandard} [get_ports {{{name}}}]"
            ]

def emit_diff_pair_xdc(p_name: str, n_name: str, p_pin: str, n_pin: str, iostandard: str) -> list[str]:
    return [
            f"set_property PACKAGE_PIN {p_pin} [get_ports {{{p_name}}}]",
            f"set_property IOSTANDARD {iostandard} [get_ports {{{p_name}}}]",
            f"set_property PACKAGE_PIN {n_pin} [get_ports {{{n_name}}}]",
            f"set_property IOSTANDARD {iostandard} [get_ports {{{n_name}}}]"
            ]

def emit_as_single_bit_signal(signal: dict[str, Any], pins: list[dict[str, Any]]) -> bool:
    """Determine if a signal should be emitted as single bit or a bus"""

    if len(pins) > 1:
        return False
    elif len(pins) == 1 and signal['as_bus'] == True:
        return False
    else:
        return True

