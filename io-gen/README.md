# Development
The pattern to follow here is
1. Validation	            Ensure input is syntactically and structurally correct
2. Flattening	            Normalize or denest complex structures (resolve defaults, refs, etc)
3. Intermediate Model	    Build logical objects that understand semantics and relationships
4. Code/Output Generation	Render structured output in the target domain (HDL, XDC, etc.)

## Validation
Validates structure and types of the YAML
- Ensures YAML matches schema
- Find bad enumeration values, catch structural issues early
- Guarantee the next stage receives only valid well-formed data

**Input** is raw user YAML
**Output** Python 

## Flattening
Normalize structured input into a uniform, flat representation per signal.
- Resolve inherited fields (e.g., iostandard from bank).
- Expand ranges, aliases, or compound forms (e.g., data[0:7] → 8 flat signals).
- Make each signal’s definition complete, explicit, and self-contained.
- Strip unused context to focus only on signal-level truth.

**Input** Validated YAML dict
**Output** List or dict of flat signal records (e.g. List[Dict[str, str]])
