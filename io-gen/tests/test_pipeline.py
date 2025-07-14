import yaml
import json
from pathlib import Path
from io_gen.validator import validate

from jsonschema.exceptions import ValidationError

FIXTURE = Path("tests/fixtures/pipeline/arty-z7-20.yaml")

def test_pipeline_smoke():
    # Load YAML
    with open(FIXTURE) as f:
        data = yaml.safe_load(f)

    # Stage 1: Schema validation
    try:
        validate(data)
    except ValidationError as e:
        print("Validation failed!")
        print("Path:", list(e.path))            # Points to the failing object (e.g. ['signals', 2, 'comment', 'hdl'])
        print("Message:", e.message)            # Human-readable error
        print("Schema path:", list(e.schema_path))  # Which rule failed
        raise
