#!/usr/bin/python3

import json
import yaml
from jsonschema import validate, ValidationError

with open("./schema/schema.json") as s:
    schema = json.load(s)

with open("./examples/test-basic.yaml") as y:
    data = yaml.safe_load(y)

try:
    validate(instance=data, schema=schema)
    print("✅ YAML is valid")
except ValidationError as e:
    print("❌ YAML is invalid")
    print(e.message)

