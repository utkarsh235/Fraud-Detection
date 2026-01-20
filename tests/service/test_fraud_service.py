import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from src.service.fraud_service import FraudService

@patch("src.service.fraud_service.FraudDetection")
@patch("src.service.fraud_service.TransactionPreprocessor")
@patch("src.service.fraud_service.TransactionTransformer")
@patch("src.service.fraud_service.TransactionValidator")
@patch("src.service.fraud_service.TransactionRepository")
def test_detect_happy_path(
    mock_repo_cls,
    mock_validator,
    mock_transformer,
    mock_preprocessor_cls,
    mock_fraud_detection_cls,
):
    # Arrange
    transactions = [MagicMock()]
    df = pd.DataFrame({"amount": [10.0]})
    processed_df = pd.DataFrame({"amount": [0.0]})
    flagged = ["tx-1"]

    # Repository mock
    mock_repo = MagicMock()
    mock_repo.find_all.return_value = df
    mock_repo_cls.return_value = mock_repo

    # Transformer mock
    mock_transformer.to_dataframe.return_value = df

    # Preprocessor mock
    mock_preprocessor = MagicMock()
    mock_preprocessor.normalize_amount.return_value = processed_df
    mock_preprocessor_cls.return_value = mock_preprocessor

    # FraudDetection mock
    mock_fd = MagicMock()
    mock_fd.get_flagged_transactions.return_value = flagged
    mock_fraud_detection_cls.return_value = mock_fd

    service = FraudService("fake/path.csv")

    # Act
    result = service.detect(transactions)

    # Assert – validation
    mock_validator.validate.assert_called_once_with(transactions)

    # Assert – transformation
    mock_transformer.to_dataframe.assert_called_once_with(transactions)

    # Assert – persistence
    mock_repo.save.assert_called_once_with(df)
    mock_repo.find_all.assert_called_once()

    # Assert – preprocessing
    mock_preprocessor.normalize_amount.assert_called_once_with(df)

    # Assert – fraud detection
    mock_fraud_detection_cls.assert_called_once_with(
        method="naive",
        data=processed_df
    )
    mock_fd.check.assert_called_once()
    mock_fd.get_flagged_transactions.assert_called_once()

    assert result == flagged


@patch("src.service.fraud_service.TransactionValidator")
@patch("src.service.fraud_service.TransactionRepository")
def test_detect_stops_on_validation_error(
    mock_repo_cls,
    mock_validator,
):
    mock_validator.validate.side_effect = ValueError("invalid")

    service = FraudService("fake/path.csv")

    with pytest.raises(ValueError):
        service.detect([MagicMock()])

    # Repository should never be used
    mock_repo_cls.assert_called_once()


@patch("src.service.fraud_service.FraudDetection")
@patch("src.service.fraud_service.TransactionPreprocessor")
@patch("src.service.fraud_service.TransactionTransformer")
@patch("src.service.fraud_service.TransactionValidator")
@patch("src.service.fraud_service.TransactionRepository")
def test_detect_returns_empty_when_no_fraud_found(
    mock_repo_cls,
    mock_validator,
    mock_transformer,
    mock_preprocessor_cls,
    mock_fraud_detection_cls,
):
    df = pd.DataFrame({"amount": [1.0]})

    mock_repo = MagicMock()
    mock_repo.find_all.return_value = df
    mock_repo_cls.return_value = mock_repo

    mock_transformer.to_dataframe.return_value = df

    mock_preprocessor = MagicMock()
    mock_preprocessor.normalize_amount.return_value = df
    mock_preprocessor_cls.return_value = mock_preprocessor

    mock_fd = MagicMock()
    mock_fd.get_flagged_transactions.return_value = []
    mock_fraud_detection_cls.return_value = mock_fd

    service = FraudService("fake/path.csv")

    result = service.detect([MagicMock()])

    assert result == []

