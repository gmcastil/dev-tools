#!/usr/bin/python3

import os
import json
import yaml
from jsonschema import Draft202012Validator, RefResolver

# Paths
schema_dir = os.path.join(os.path.dirname(__file__), "schema")
schema_path = os.path.join(schema_dir, "schema.json")
yaml_path = os.path.join(os.path.dirname(__file__), "examples", "test-basic.yaml")

# Load schema and instance
with open(schema_path) as f:
    schema = json.load(f)
with open(yaml_path) as f:
    instance = yaml.safe_load(f)

# Use base URI to resolve $ref correctly
resolver = RefResolver(base_uri=f"file://{schema_dir}/", referrer=schema)

# Validate
Draft202012Validator(schema, resolver=resolver).validate(instance)
print("✅ YAML is valid")

