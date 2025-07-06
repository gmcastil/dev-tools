from tests.fixtures.parsed_data import get_signals, get_banks
from io_gen.signal_table import extract_signal_table
from io_gen.bank_table import extract_bank_table
from io_gen.pin_table import extract_pin_table

# def test_extract_pin_table_from_pipeline_input():
#     signals = get_signals()
#     banks = get_banks()
#     signal_table = extract_signal_table(signals)
#     bank_table = extract_bank_table(banks)
#     pin_table = extract_pin_table(signals, signal_table, bank_table)

#     assert any(p["name"] == "data" and p["index"] == 1 for p in pin_table)

