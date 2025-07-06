from collections import defaultdict
from typing import List, Dict, Any

from io_gen.validator import load_enum_values, DEFS_DIR

# Supported buffer direction, buffer types, and IOSTANDARDS. These are duplications
# to some degree what is in the JSON schema.
ENUM_DIRECTION = set(load_enum_values(DEFS_DIR / "direction.json"))
ENUM_BUFFER = set(load_enum_values(DEFS_DIR / "buffer.json"))
ENUM_IOSTANDARD = set(load_enum_values(DEFS_DIR / "iostandard.json"))

def validate_flattened(flattened: List[Dict[str, Any]]) -> None:
    """Ensures each member of flattened signal list is valid and consistent

    Checks:
    - Required fields are present
    - Only pin or p/n present, not both
    - Index is non-negative
    - Name/index pair is unique
    - Physical pins (or diff pairs) are not reused

    """
    seen_names_index = set()
    used_pins = set()

    for sig in flattened:
        # Each signal needs to have these fields
        assert isinstance(sig['name'], str) and sig['name']
        assert isinstance(sig['index'], int) and sig['index'] >= 0
        assert sig['direction'] in ENUM_DIRECTION
        assert sig['buffer'] in ENUM_BUFFER
        assert sig['iostandard'] in ENUM_IOSTANDARD
        assert isinstance(sig['as_bus'], bool)

        # A name and index tuple is a unique way to identify duplicate signals
        # because every signal is guaranteed to contain an index.
        key = (sig['name'], sig['index'])
        if key in seen_names_index:
            msg = f"Duplicate signal name / index found: {key}"
            raise ValueError(msg)
        seen_names_index.add(key)

        # Check that pins are unique and not reused or doubled
        if 'pin' in sig:
            assert isinstance(sig['pin'], str)
            pin_key = sig['pin']
        elif 'p' in sig and 'n' in sig:
            assert isinstance(sig['p'], str)
            assert isinstance(sig['n'], str)
            pin_key = (sig['p'], sig['n'])
        else:
            msg = f"Signal missing required fields: {sig}"
            raise ValueError(msg)

        if pin_key in used_pins:
            msg = f"Duplicate package pin found: {pin_key}"
            raise ValueError(msg)
        used_pins.add(pin_key)

        # Check that indices are 0-based contiguous per signal
        signal_indices = defaultdict(set)
        for sig in flattened:
            signal_indices[sig["name"]].add(sig["index"])

        for name, indices in signal_indices.items():
            expected = set(range(len(indices)))
            if indices != expected:
                raise ValueError(f"Signal '{name}' has non-contiguous indices: {sorted(indices)}")


