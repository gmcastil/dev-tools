import pytest
import yaml

from jsonschema.exceptions import ValidationError

from io_gen.validator import validate
from io_gen.normalize import normalize
from io_gen.annotate import annotate
from io_gen.check import check

def run_pipeline(data):
    validate(data)
    result = normalize(data)
    result = annotate(result)
    check(result)

def test_valid_single_pin():
    data = yaml.safe_load("""
title: Test
part: xc7z010clg400-1
banks:
  - bank: 34
    iostandard: LVCMOS33
    performance: HR
signals:
  - name: btn
    direction: in
    buffer: ibuf
    bank: 34
    pin: "A1"
""")
    run_pipeline(data)


def test_valid_pins_array_with_bus_true():
    data = yaml.safe_load("""
title: Test
part: xc7z010clg400-1
banks:
  - bank: 34
    iostandard: LVCMOS33
    performance: HR
signals:
  - name: sw
    direction: in
    buffer: ibuf
    bank: 34
    pins: ["A2", "A3", "A4"]
    bus: true
""")
    run_pipeline(data)


def test_valid_pinset_differential_pair():
    data = yaml.safe_load("""
title: Test
part: xc7z010clg400-1
banks:
  - bank: 34
    iostandard: LVDS
    performance: HR
signals:
  - name: clk_in
    direction: in
    buffer: ibufds
    bank: 34
    pinset:
      p: "C1"
      n: "C2"
""")
    run_pipeline(data)


def test_override_iostandard():
    data = yaml.safe_load("""
title: Test
part: xc7z010clg400-1
banks:
  - bank: 34
    iostandard: LVCMOS33
    performance: HR
signals:
  - name: led
    direction: out
    buffer: obuf
    bank: 34
    pin: "B1"
    iostandard: LVCMOS18
""")
    run_pipeline(data)


def test_error_multibit_bus_false():
    data = yaml.safe_load("""
title: BadBus
part: xc7z010clg400-1
banks:
  - bank: 34
    iostandard: LVCMOS33
    performance: HR
signals:
  - name: bad
    direction: out
    buffer: obuf
    bank: 34
    pins: ["B2", "B3"]
    bus: false
""")
    with pytest.raises(Exception):
        run_pipeline(data)

def test_inherited_iostandard():
    data = yaml.safe_load("""
title: InheritIO
part: xc7z010clg400-1
banks:
  - bank: 35
    iostandard: LVCMOS18
    performance: HR
signals:
  - name: btn2
    direction: in
    buffer: ibuf
    bank: 35
    pin: "D5"
""")
    run_pipeline(data)

def test_valid_pinset_array():
    data = yaml.safe_load("""
title: DifferentialArray
part: xc7z010clg400-1
banks:
  - bank: 36
    iostandard: LVDS
    performance: HR
signals:
  - name: diff_bus
    direction: in
    buffer: ibufds
    bank: 36
    pinset:
      p: ["C1", "C3", "C5"]
      n: ["C2", "C4", "C6"]
    bus: true
""")
    run_pipeline(data)

def test_pinset_mismatched_arrays():
    data = yaml.safe_load("""
title: BadDiffPair
part: xc7z010clg400-1
banks:
  - bank: 36
    iostandard: LVDS
    performance: HR
signals:
  - name: mismatch
    direction: in
    buffer: ibufds
    bank: 36
    pinset:
      p: ["C1", "C3"]
      n: ["C2", "C4", "C5"]
""")
    with pytest.raises(ValueError, match="must be equal lengths"):
        run_pipeline(data)

def test_missing_pin_fields():
    data = yaml.safe_load("""
title: MissingPins
part: xc7z010clg400-1
banks:
  - bank: 36
    iostandard: LVCMOS25
    performance: HR
signals:
  - name: broken
    direction: out
    buffer: obuf
    bank: 36
""")
    with pytest.raises(Exception):
        run_pipeline(data)

def test_missing_iostandard():
    data = yaml.safe_load("""
title: NoIOStandard
part: xc7z010clg400-1
banks:
  - bank: 37
    performance: HR
    # no iostandard
signals:
  - name: orphan
    direction: out
    buffer: obuf
    bank: 37
    pin: "F7"
""")
    with pytest.raises(ValidationError, match="iostandard.*required property"):
        run_pipeline(data)

