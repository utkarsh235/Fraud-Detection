import pandas as pd
import pytest

from src.processing.transformer import TransactionTransformer
from src.domain.transaction import Transaction

def test_to_dataframe_creates_dataframe_with_expected_columns():
    transactions = [
        Transaction("tx-1", 100.0, "USD"),
        Transaction("tx-2", 50.5, "EUR"),
    ]

    df = TransactionTransformer.to_dataframe(transactions)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["transaction_id", "amount", "currency"]

def test_to_dataframe_contains_correct_values():
    transactions = [
        Transaction("tx-1", 100.0, "USD"),
        Transaction("tx-2", 50.5, "EUR"),
    ]

    df = TransactionTransformer.to_dataframe(transactions)

    assert df.iloc[0]["transaction_id"] == "tx-1"
    assert df.iloc[0]["amount"] == 100.0
    assert df.iloc[0]["currency"] == "USD"

    assert df.iloc[1]["transaction_id"] == "tx-2"
    assert df.iloc[1]["amount"] == 50.5
    assert df.iloc[1]["currency"] == "EUR"

def test_to_dataframe_with_empty_list_returns_empty_dataframe():
    df = TransactionTransformer.to_dataframe([])

    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert list(df.columns) == []

def test_to_dataframe_supports_duck_typed_objects():
    class DummyTransaction:
        def __init__(self, transaction_id, amount, currency):
            self.transaction_id = transaction_id
            self.amount = amount
            self.currency = currency

    transactions = [
        DummyTransaction("tx-1", 10.0, "USD")
    ]

    df = TransactionTransformer.to_dataframe(transactions)

    assert df.iloc[0]["transaction_id"] == "tx-1"

def test_to_dataframe_raises_if_attribute_missing():
    class InvalidTransaction:
        def __init__(self):
            self.transaction_id = "tx-1"

    transactions = [InvalidTransaction()]

    with pytest.raises(AttributeError):
        TransactionTransformer.to_dataframe(transactions)
