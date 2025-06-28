"""
Flatten and normalize validated input data before generating HDL or XDC

Responsibilities:
- Transform structured YAML data into a flat list of signal descriptions.
- Attach bank defaults (e.g. IOSTANDARD) to each signal.
- Validate logical consistency (e.g., pad required for non-internal signals).

Input:
- Validated dict from `validator`

Output:
- List of dict with each entry a discrete signal that is ready for emission

"""

