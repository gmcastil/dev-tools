import yaml
import json

from io_gen.flatten import flatten_signals, flatten_banks
from io_gen.validator import validate

from tests.utils import *

def test_flatten_matches_expected_fixture():
    with open("tests/fixtures/pipeline_input.yaml") as f:
        raw_yaml = yaml.safe_load(f)

    validate(raw_yaml)
    banks = flatten_banks(raw_yaml["banks"])
    result = flatten_signals(raw_yaml["signals"], banks)

    with open("tests/fixtures/expected_flatten_signals.json") as f:
        expected = json.load(f)

    sorted_result = normalize_dicts(sorted(result, key=sort_key))
    sorted_expected = normalize_dicts(sorted(expected, key=sort_key))
    assert sorted_result == sorted_expected
