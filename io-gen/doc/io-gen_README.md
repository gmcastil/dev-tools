# io-gen

`io-gen` is a YAML-to-HDL/XDC compiler for FPGA IO constraints.

It transforms structured YAML into pin-level HDL definitions and XDC constraints in a multistage pipeline:

## Pipeline Overview

1. **Validation** – Checks user input against a strict JSON schema
2. **Flattening** – Expands user-defined signals into atomic pin or differential pair entries
3. **Annotation** – Computes derived properties like `width`
4. **Check** – Enforces semantic correctness and warns about questionable constructs
5. **Emit** – Generates HDL and XDC output

## Signal Types

Each signal must be one of the following:
- `pin` – scalar, single-ended
- `pins` – array of single-ended bits
- `pinset` – scalar or array of differential pairs
- `multibank` – cross-bank group of `pin` or `pinset` entries with `offset` and `width`

## Special Fields

- `bus: true | false`
  - Only valid for scalar `pin` or `pinset`
  - Forces a single-bit signal to be treated as a bus of width 1
  - Required for those cases; not allowed for multibit signals or `pins`, `pinset[]`, or `multibank`

- `width`
  - **Required** only for `multibank`
  - Inferred automatically elsewhere

- `offset`
  - Only used within `multibank` fragments
  - Must form a complete, gap-free, non-overlapping set of indices from `0` to `width - 1`

## Banks Dictionary

After validation, `banks` becomes a lookup table keyed by bank number:

```python
{
  34: {
    "iostandard": "LVCMOS33",
    "performance": "HR",       # optional
    "comment": "User note"     # optional
  },
  35: {
    "iostandard": "LVCMOS18"
  }
}
```

This LUT is passed to the flattening functions.

- Signals may omit `iostandard` and inherit it from their bank
- `multibank` signals may inherit **different** `iostandard` values per fragment
  - This is valid and supported
  - The `check` stage emits an **info-level** message if differing IOSTANDARDs are inherited

## Multibank Rules

- A `multibank` signal must use either all single-ended (`pin`, `pins`) or all differential (`pinset`) signal forms
- You may not mix `pin` with `pinset`
- You may repeat and reorder banks arbitrarily
- Each fragment must specify both `offset` and a valid number of pins/pairs
- The combined flattened result must yield exactly `width` entries, with no gaps or duplicates

## Design Philosophy

- The tool uses a pin- or pin-pair–level internal representation
- Indexing is always explicit
- All stages are test-driven and data-first
- Output is intentionally agnostic to synthesis tools (Vivado, etc.)
