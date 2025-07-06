import pytest
from io_gen.bank_table import extract_bank_table, validate_bank_table
from tests.fixtures import get_banks

def test_extract_bank_table_valid():
    banks = get_banks()
    bank_table = extract_bank_table(banks)

    assert isinstance(bank_table, dict)
    assert 34 in bank_table
    assert bank_table[34]["iostandard"] == "LVCMOS33"
    assert bank_table[34]["performance"] == "HD"


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

