import pytest
import yaml
from io_gen import validator
from jsonschema import ValidationError

def test_valid_yaml_is_accepted():
    # Sample minimal valid YAML structure
    raw_yaml = """
    title: arty-z7-20
    part: xc7z020clg400-1
    banks:
      - bank: 34
        iostandard: LVCMOS33
    signals:
      - name: led
        pad: K17
        direction: out
        bank: 34
        buffer: obuf
    """

    parsed = yaml.safe_load(raw_yaml)
    validated = validator.validate_yaml_dict(parsed)
    assert isinstance(validated, dict)
    assert validated["title"] == "arty-z7-20"

def test_invalid_yaml_missing_field_raises():
    raw_yaml = """
    title: arty-z7-20
    part: xc7z020clg400-1
    banks:
      - bank: 34
        iostandard: LVCMOS33
    signals:
      - name: led
        pad: K17
        bank: 34
        buffer: obuf
    """  # ← missing `direction`

    parsed = yaml.safe_load(raw_yaml)

    with pytest.raises(ValidationError):
        validator.validate_yaml_dict(parsed)

