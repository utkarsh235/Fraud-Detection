import pandas as pd
import numpy as np
import pytest
from unittest.mock import MagicMock, patch

from src.detect import (
    validateData,
    transformData,
    preprocessing,
    normalizeAmount,
    detect,
)
from src.dataclass.transaction import Transaction

def test_validateData_valid_transactions():
    data = [
        {"transaction_id": "tx-1", "amount": 10},
        {"transaction_id": "tx-2", "amount": 20},
    ]

    validateData(data)  # should not raise


def test_validateData_missing_amount():
    data = [
        {"transaction_id": "tx-1", "amount": None},
    ]

    with pytest.raises(Exception):
        validateData(data)


def test_transformData_creates_dataframe_from_transactions():
    data = [
        {"transaction_id": "tx-1", "amount": 10, "currency": "USD"},
        {"transaction_id": "tx-2", "amount": 20, "currency": "EUR"},
    ]

    df = transformData(data)

    assert list(df.columns) == ["transaction_id", "amount", "currency"]
    assert len(df) == 2
    assert df.iloc[0]["transaction_id"] == "tx-1"
    assert df.iloc[1]["amount"] == 20

def test_normalizeAmount_returns_scaled_array():
    amounts = pd.Series([10, 20, 30])

    result = normalizeAmount(amounts)

    assert isinstance(result, np.ndarray)
    assert result.shape == (3, 1)

def test_preprocessing_normalizes_amount_column():
    df = pd.DataFrame({
        "transaction_id": ["tx-1", "tx-2"],
        "amount": [10, 20],
        "currency": ["USD", "USD"],
    })

    processed = preprocessing(df)
    assert isinstance(processed["amount"].iloc[0], (float, np.floating))
    assert processed["amount"].mean() == pytest.approx(0.0)

@patch("src.detect.persistTransactions")
@patch("src.detect.getAllTransactions")
@patch("src.detect.FraudDetection")
def test_detect_returns_flagged_transactions(
    mock_fraud_class,
    mock_get_all,
    mock_persist,
):
    data = [
        {"transaction_id": "tx-1", "amount": -10, "currency": "USD"},
    ]

    df = pd.DataFrame({
        "transaction_id": ["tx-1"],
        "amount": [-10],
        "currency": ["USD"],
    })

    mock_get_all.return_value = df

    fraud_instance = MagicMock()
    fraud_instance.get_flagged_transactions.return_value = ["tx-1"]
    mock_fraud_class.return_value = fraud_instance

    result = detect(data)

    mock_persist.assert_called_once()
    fraud_instance.check.assert_called_once()
    assert result == ["tx-1"]

