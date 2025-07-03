import yaml
import json
from io_gen.flatten import flatten_signals
from io_gen.validator import validate

def test_flatten_matches_expected_fixture():
    with open("tests/fixtures/pipeline_input.yaml") as f:
        raw_yaml = yaml.safe_load(f)

    validate(raw_yaml)
    result = flatten_signals(raw_yaml["signals"], raw_yaml["banks"])

    with open("tests/fixtures/expected_flatten_output.json") as f:
        expected = json.load(f)

    assert result == expected

