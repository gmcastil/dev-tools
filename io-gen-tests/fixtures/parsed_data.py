import yaml
import pathlib

FIXTURE_PATH = pathlib.Path(__file__).parent / "pipeline_input.yaml"

def load_pipeline_input():
    with open(FIXTURE_PATH, "r") as f:
        return yaml.safe_load(f)

# Convenience accessors to return the signals and banks from the YAML, so I don't
# have to go diving in there each time I need data.
def get_signals():
    return load_pipeline_input()["signals"]

def get_banks():
    return load_pipeline_input()["banks"]

