import pytest
from io_gen.bank_table import extract_bank_table, validate_bank_table
from tests.fixtures import get_banks



def test_extract_bank_table_valid():
    banks = get_banks()
    bank_table = extract_bank_table(banks)

    expected = {
            34: {
                "iostandard": "LVCMOS33",
                "performance": "HD",
                "comment": "Primary high-drive bank"
                },
            35: {
                "iostandard": "LVDS",
                "performance": "HR",
                "comment": "Differential-capable bank"
                },
            36: {
                "iostandard": "LVCMOS18",
                "performance": "HR",
                "comment": "Low-voltage bank"
                }
            }

    assert expected == bank_table

def test_validate_bank_table_valid():
    banks = get_banks()
    bank_table = extract_bank_table(banks)

    # Should not raise
    validate_bank_table(bank_table)

def test_missing_iostandard_raises():
    bad = {
        34: {
            "performance": "HR"
        }
    }
    with pytest.raises(ValueError, match="missing required key 'iostandard'"):
        validate_bank_table(bad)


def test_invalid_performance_type_raises():
    bad = {
        34: {
            "iostandard": "LVCMOS33",
            "performance": "FOO"
        }
    }
    with pytest.raises(ValueError, match="invalid performance type"):
        validate_bank_table(bad)

