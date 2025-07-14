# YAML Schema Reference (for `io-gen`)

This section documents the structure, rules, and conventions for defining FPGA I/O using the `io-gen` YAML format. The schema is enforced using [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema), and validation occurs before downstream stages like flattening or emission.

## Top-Level Fields

| Field     | Type     | Description                                      |
|-----------|----------|--------------------------------------------------|
| `title`   | string   | Title or name of the I/O description             |
| `part`    | string   | FPGA part name (e.g., `xc7z020clg400-1`)         |
| `signals` | array    | List of signal objects (see below)              |
| `banks`   | object   | Mapping of bank numbers to attributes           |

## Signal Definitions

Each signal must define one of the following structures:
- `pins`: single-ended
- `pinset`: differential pair
- `multibank`: single-ended or differential pair arrays split across multiple banks

| Field        | Type         | Required?     | Notes                                                              |
|--------------|--------------|---------------|--------------------------------------------------------------------|
| `name`       | string       | Always        | Unique signal name                                                 |
| `direction`  | string       | Usually       | `"in"`, `"out"`, `"inout"` — required unless `generate: false`     |
| `buffer`     | string       | Usually       | One of `"obuf"`, `"ibuf"`, `"obufds"`, `"ibufds"`                  |
| 'iostandard' | string       | Conditionally | TBD: Need to describe the overriding ehavior here                  |
| `generate`   | boolean      | Optional      | Defaults to `true`. If `false`, only `name` is required            |
| `width`      | integer ≥1   | Conditionally | Required for buses and multibank. Optional for scalars (if present, must equal 1) |
| `comment`    | object       | Optional      | Optional comment block with `hdl` and/or `xdc` fields              |
| `group`      | string       | Optional      | Classification for grouping (e.g., `clock`, `uart`, etc.)          |

## `pins` (Single-Ended)

- Scalar:

  ```yaml
  pins: A1
  ```

  No `width` required or enforced.

- Bus:

  ```yaml
  pins: [A1, A2, A3]
  width: 3
  ```

  `width` is required.

## `pinset` (Differential Pair)

- Scalar differential:

  ```yaml
  pinset:
    p: C1
    n: C2
  ```

- Differential bus:

  ```yaml
  pinset:
    p: [C1, C2]
    n: [C3, C4]
    width: 2
  ```

## `multibank`

Defines a bus distributed across multiple I/O banks.

```yaml
multibank:
  - bank: 34
    pins: [A1, A2]
    offset: 0
  - bank: 35
    pins: [B1, B2]
    offset: 2
width: 4
```

- Each fragment must include:
  - `bank`: bank number
  - exactly one of: `pin`, `pins`, or `pinset`
  - `offset`: starting index of this fragment within the full signal
- Total width must match the sum of all fragment widths
- All fragments will be flattened and annotated individually
- Mixed multibank signals are not supported (e.g., single-ended pins in one bank and differential pairs in another)

## Behavior Notes

- `generate: false` means the signal is present in the YAML but will be ignored during flattening and emission — only `name` is required in this case. This is largely intended to document unused pins on the schematic that may appear in other (e.g., vendor) XDC sources or documentation.
- `width` is optional for scalars, but when present must be exactly 1. This is not enforced during schema validation, but is checked later.
- `comment.xdc` and `comment.hdl` allow optional human-readable comments to be emitted in generated output.

## Schema Enforcement

The schema enforces:
- Mutual exclusivity between `pins`, `pinset`, and `multibank`
- Proper width requirements for bus-style pins and pinsets
- Use of only allowed values for enums like `direction`, `buffer`, `group`, etc.
- No additional fields are permitted (i.e., extra keys will cause validation failure)

Defaults (like `generate: true`) are treated as implicit and must be handled by the tool logic — they are not inserted by the validator.
