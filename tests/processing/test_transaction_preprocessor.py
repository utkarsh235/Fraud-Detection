import pandas as pd
import numpy as np
import pytest

from src.processing.preprocessor import TransactionPreprocessor

def test_normalize_amount_standardizes_values():
    df = pd.DataFrame({
        "transaction_id": ["tx-1", "tx-2", "tx-3"],
        "amount": [10.0, 20.0, 30.0],
        "currency": ["USD", "USD", "USD"]
    })

    preprocessor = TransactionPreprocessor()
    result = preprocessor.normalize_amount(df.copy())

    amounts = result["amount"].values.astype(float)

    assert abs(amounts.mean()) < 1e-7
    assert abs(amounts.std(ddof=0) - 1.0) < 1e-7

def test_normalize_amount_preserves_column_shape():
    df = pd.DataFrame({
        "amount": [100.0, 200.0]
    })

    preprocessor = TransactionPreprocessor()
    result = preprocessor.normalize_amount(df.copy())

    assert result["amount"].ndim == 1
    assert len(result["amount"]) == 2

def test_normalize_amount_does_not_modify_other_columns():
    df = pd.DataFrame({
        "transaction_id": ["tx-1", "tx-2"],
        "amount": [5.0, 15.0],
        "currency": ["USD", "EUR"]
    })

    preprocessor = TransactionPreprocessor()
    result = preprocessor.normalize_amount(df.copy())

    pd.testing.assert_series_equal(
        result["transaction_id"],
        df["transaction_id"]
    )
    pd.testing.assert_series_equal(
        result["currency"],
        df["currency"]
    )

def test_normalize_amount_modifies_dataframe_in_place():
    df = pd.DataFrame({"amount": [1.0, 2.0, 3.0]})

    preprocessor = TransactionPreprocessor()
    returned_df = preprocessor.normalize_amount(df)

    assert returned_df is df

def test_normalize_amount_missing_amount_column_raises_key_error():
    df = pd.DataFrame({
        "transaction_id": ["tx-1"]
    })

    preprocessor = TransactionPreprocessor()

    with pytest.raises(KeyError):
        preprocessor.normalize_amount(df)

def test_normalize_amount_non_numeric_amount_raises_value_error():
    df = pd.DataFrame({
        "amount": ["invalid", "data"]
    })

    preprocessor = TransactionPreprocessor()

    with pytest.raises(ValueError):
        preprocessor.normalize_amount(df)
