from typing import Any

from io_gen.pin_table import get_pins_by_signal


def emit_xdc(
    signal_table: list[dict[str, Any]], pin_table: list[dict[str, Any]]
) -> list[str]:
    """Constructs XDC constraints from signal table and flattend pin table"""

    output_xdc = []

    # Iterate over the signal table by signal name
    for signal in signal_table:
        sig_name = signal["name"]
        pins = get_pins_by_signal(sig_name, pin_table)

        # Start the signal with the XDC comment
        xdc_comment = get_xdc_comment(signal)
        if xdc_comment:
            output_xdc.append(xdc_comment)

        if signal["diff_pair"]:
            output_xdc.extend(emit_xdc_diff(pins))
        else:
            output_xdc.extend(emit_xdc_single(pins))

        # Finish the signal text with an empty line
        output_xdc.append("")

    return output_xdc


def emit_xdc_single(pins: list[dict[str, Any]]) -> list[str]:
    """Returns a list of pin constraints for singled ended signals"""
    xdc_lines = []
    for pin in sorted(pins, key=lambda entry: entry["index"]):
        # set_property PACKAGE_PIN A1 [get_ports {steak_sauce_pad}]
        port_name = get_xdc_single_port_name(pin)
        pkg_pin_str = (
            f"set_property PACKAGE_PIN {pin['pin']} [get_ports {{{port_name}}}]"
        )
        xdc_lines.append(pkg_pin_str)

        # set_property IOSTANDARD LVCMOS33 [get_ports {steak_sauce_pad}]
        iostandard = get_xdc_iostandard(pin)
        iostandard_str = (
            f"set_property IOSTANDARD {iostandard} [get_ports {{{port_name}}}]"
        )
        xdc_lines.append(iostandard_str)

    return xdc_lines


def emit_xdc_diff(pins: list[dict[str, Any]]) -> list[str]:
    """Returns a list of pin constraints for diff signals"""
    xdc_lines = []
    for pin in sorted(pins, key=lambda entry: entry["index"]):
        # set_property PACKAGE_PINS A1 [get_port {steak_sauce_p}]
        # set_property PACKAGE_PINS A2 [get_port {steak_sauce_n}]
        port_p, port_n = get_xdc_port_names_diff(pin)
        pkg_pin_p_str = f"set_property PACKAGE_PIN {pin['p']} [get_ports {{{port_p}}}]"
        pkg_pin_n_str = f"set_property PACKAGE_PIN {pin['n']} [get_ports {{{port_n}}}]"

        # set_property IOSTANDARD LVCMOS33 [get_ports {steak_sauce_p}]
        # set_property IOSTANDARD LVCMOS33 [get_ports {steak_sauce_n}]
        iostandard = get_xdc_iostandard(pin)
        iostandard_str_p = (
            f"set_property IOSTANDARD {iostandard} [get_ports {{{port_p}}}]"
        )
        iostandard_str_n = (
            f"set_property IOSTANDARD {iostandard} [get_ports {{{port_n}}}]"
        )

        xdc_lines.append(pkg_pin_p_str)
        xdc_lines.append(iostandard_str_p)
        xdc_lines.append(pkg_pin_n_str)
        xdc_lines.append(iostandard_str_n)

    return xdc_lines


def get_xdc_comment(signal: dict[str, Any]) -> str | None:
    """Return XDC comment string if present, else None."""
    comment = signal.get("comment", {}).get("xdc")
    return f"# {comment}" if comment else None


# Port name formatting is handled by a dedicated helper function.
# This cleanly encapsulates the logic for whether to emit `foo` or `foo[0]`,
# based on the `bus` flag. It avoids cluttering the emitter with conditionals,
# and handles degenerate 1-bit buses in a centralized, consistent way.


def get_xdc_single_port_name(pin: dict[str, Any]) -> str:
    """Return the port name for a single-ended pin"""
    base = f"{pin['name']}_pad"
    if pin["bus"]:
        return f"{base}[{pin['index']}]"
    else:
        return f"{base}"


def get_xdc_port_names_diff(pin: dict[str, Any]) -> tuple[str, str]:
    """Return the port names for a differential pair"""
    base_p = f"{pin['name']}_p"
    base_n = f"{pin['name']}_n"
    if pin["bus"]:
        return f"{base_p}[{pin['index']}]", f"{base_n}[{pin['index']}]"
    else:
        return base_p, base_n


def get_xdc_iostandard(pin: dict[str, Any]) -> str:
    """Return the IOSTANDARD property for the pin or pin pair"""
    return pin["iostandard"]
