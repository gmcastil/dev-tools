# io-gen Tool Design Overview

This document describes the pipeline stages in `io-gen`, their purpose,
expectations, and outputs. It defines the structure of the tool so future
development can proceed without needing to mentally contain the entire
implementation.

     ---

## Goal
Generate HDL and XDC constraints for top-level FPGA signals from structured
YAML descriptions.

     ---

## Pipeline Stages
Data is transformed from YAML to an internal data model, with various structural and semantic checks along the way, in several stages.

### 1. **Validation (`validate`)**

     * **Input**: Raw user-provided YAML.
     * **Purpose**: Ensure the structure conforms to the JSON schema.
     * **Enforces**:

    * Required fields (`name`, `direction`, etc.)
    * Type correctness (e.g., `pins` must be an array)
    * Disallow unknown fields (`additionalProperties: false`)
    * Mutual exclusivity (`pin` vs `pins`, etc.)
    * **Output**: Structurally valid dictionary (parsed YAML).

    ---

### 2. **Normalization (`normalize`)**

    * **Input**: Validated data from `validate()`
    * **Purpose**: Flatten bank and signal definitions, apply inheritance.
    * **Performs**:
    * Convert list of banks → dict keyed by bank number
    * Apply inherited fields from banks to signals (e.g., `iostandard`)
    * Preserve optional fields like `group`, `bus`
    * **Does NOT**:

* Infer derived fields (e.g., width)
    * Modify structure for codegen
    * **Output**: Clean, enriched signal list with resolved fields.

    ---

### 3. **Annotation (`annotate`)**

    * **Input**: Normalized dataset
    * **Purpose**: Add derived fields, mainly `width`, and validate form.
    * **Performs**:

    * Use `annotate_width()` to infer bit width from `pin`/`pins`/`pinset`
* Validate shape consistency (e.g., matching array lengths in pinsets)
    * Honor `bus: true` to resolve ambiguity in width-1 cases
    * **Output**: Annotated dataset with `width` and other derived values

    ---

### 4. **Semantic Check (`check`)**

    * **Input**: Annotated dataset
    * **Purpose**: Enforce semantic rules required for safe codegen.
    * **Checks**:

    * Duplicate signal names
    * Pin reuse across signals or vector overlaps
* Pinset consistency (already checked in annotate)
    * TODO: incompatible direction/buffer combos, conflicting assignments, bank cross-checks
    * **Output**: Raises `ValueError` on invalid designs, returns None if OK

    ---

### 5. **Codegen (`emit_hdl`, `emit_xdc`)** *(Future)*

    * **Input**: Checked dataset
    * **Purpose**: Generate synthesizable HDL and constraint files
    * **Uses**:

    * `name`, `width`, `direction`, `buffer` for HDL port declarations
    * `pin`, `pins`, `pinset`, `bank`, `iostandard` for XDC
    * **Output**: Text files written to disk or returned as strings

    ---

## Core Design Principles

    * **Stage purity**: each stage should not mutate its input.
    * **Validation upfront**: YAML is schema-checked before any logic runs.
    * **Annotation is additive**: derive, don’t override.
    * **Check is the final gate**: only passing datasets are eligible for codegen.

    ---

## Contracts Between Stages

    | From → To                | Required Guarantees                                        |
    | ------------------------ | ---------------------------------------------------------- |
    | `validate` → `normalize` | Schema-valid structure (e.g., all required fields present) |
    | `normalize` → `annotate` | Flattened, inherited, correctly typed signals              |
    | `annotate` → `check`     | Width known, form valid (pinset lengths match, etc.)       |
    | `check` → `emit_*`       | No conflicts, names and pins are unique                    |

    ---

    This document serves as the foundation for understanding and extending `io-gen`. All stages should remain independently testable and comprehensible through this lens.

