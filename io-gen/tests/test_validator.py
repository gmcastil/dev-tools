import pytest

import yaml

from jsonschema.exceptions import ValidationError

from io_gen.validator import validate

def test_valid_pin_scalar():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: led
        direction: out
        buffer: obuf
        bank: 34
        pin: A1
    """
    data = yaml.safe_load(raw_yaml)
    validate(data)

def test_valid_pins_vector():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: leds
        direction: out
        buffer: obuf
        bank: 34
        pins: [A1, A2, A3]
    """
    data = yaml.safe_load(raw_yaml)
    validate(data)

def test_valid_pinset_diff_scalar():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: clk
        direction: in
        buffer: ibuf
        bank: 34
        pinset:
          p: H1
          n: H2
    """
    data = yaml.safe_load(raw_yaml)
    validate(data)

def test_valid_pinset_diff_vector():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: data
        direction: in
        buffer: ibuf
        bank: 34
        pinset:
          p: [H1, H2]
          n: [H3, H4]
    """
    data = yaml.safe_load(raw_yaml)
    validate(data)

def test_missing_pin_and_pinset():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: led
        direction: out
        buffer: obuf
        bank: 34
    """
    with pytest.raises(ValidationError):
        validate(yaml.safe_load(raw_yaml))

def test_conflicting_pin_and_pins():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: conflict
        direction: out
        buffer: obuf
        bank: 34
        pin: A1
        pins: [A1, A2]
    """
    with pytest.raises(ValidationError):
        validate(yaml.safe_load(raw_yaml))

def test_pinset_scalar_missing_n():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: diff
        direction: in
        buffer: ibuf
        bank: 34
        pinset:
          p: H1
    """
    with pytest.raises(ValidationError):
        validate(yaml.safe_load(raw_yaml))

def test_pinset_vector_mismatched_arrays():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: diff_vec
        direction: in
        buffer: ibuf
        bank: 34
        pinset:
          p: [H1, H2, H3]
          n: [H4, H5]
    """
    validate(yaml.safe_load(raw_yaml))

def test_signal_missing_required_field():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: led
        direction: out
        # buffer is missing here
        bank: 34
        pin: A1
    """
    with pytest.raises(ValidationError, match=".*buffer.*"):
        validate(yaml.safe_load(raw_yaml))

def test_signal_unsupported_buffer():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: led
        direction: out
        # this is not supported yet
        buffer: odelay
        bank: 34
        pin: A1
    """
    with pytest.raises(ValidationError, match=".*buffer.*"):
        validate(yaml.safe_load(raw_yaml))

def test_bus_field_valid_boolean():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: valid_bus
        direction: out
        buffer: obuf
        bank: 34
        pin: A1
        bus: true
    """
    validate(yaml.safe_load(raw_yaml))

def test_pin_with_bus_true_is_valid():
    raw = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: test_sig
        direction: in
        buffer: ibuf
        bank: 34
        pin: A1
        bus: true
    """
    validate(yaml.safe_load(raw))

def test_bus_field_invalid_type():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: invalid_bus
        direction: out
        buffer: obuf
        bank: 34
        pin: A1
        bus: "yes"
    """
    with pytest.raises(ValidationError, match="bus"):
        validate(yaml.safe_load(raw_yaml))

def test_additional_properties_not_allowed():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: extra
        direction: out
        buffer: obuf
        bank: 34
        pin: A1
        foo: bar
    """
    with pytest.raises(ValidationError, match="additional properties"):
        validate(yaml.safe_load(raw_yaml))

def test_pins_too_short_rejected():
    raw_yaml = """
    title: test
    part: xc7z020
    banks:
      - bank: 34
        iostandard: LVCMOS33
        performance: HP
    signals:
      - name: short_bus
        direction: out
        buffer: obuf
        bank: 34
        pins: [A1]
    """
    with pytest.raises(ValidationError):
        validate(yaml.safe_load(raw_yaml))

