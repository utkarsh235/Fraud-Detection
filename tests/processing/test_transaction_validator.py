import pytest
from src.processing.validator import TransactionValidator
from src.domain.transaction import Transaction

def test_validate_with_valid_transactions_does_not_raise():
    transactions = [
        Transaction(transaction_id="tx-1", amount=100.0, currency="USD"),
        Transaction(transaction_id="tx-2", amount=50.5, currency="EUR"),
    ]

    # Should not raise any exception
    TransactionValidator.validate(transactions)

def test_validate_missing_transaction_id_raises_value_error():
    transactions = [
        Transaction(transaction_id=None, amount=100.0, currency="USD")
    ]

    with pytest.raises(ValueError, match="Mandatory attribute missing"):
        TransactionValidator.validate(transactions)

def test_validate_missing_amount_raises_value_error():
    transactions = [
        Transaction(transaction_id="tx-1", amount=None, currency="USD")
    ]

    with pytest.raises(ValueError, match="Mandatory attribute missing"):
        TransactionValidator.validate(transactions)

def test_validate_mixed_transactions_raises_on_invalid():
    transactions = [
        Transaction(transaction_id="tx-1", amount=100.0, currency="USD"),
        Transaction(transaction_id="tx-2", amount=None, currency="USD"),
    ]

    with pytest.raises(ValueError):
        TransactionValidator.validate(transactions)

def test_validate_empty_transaction_list_does_not_raise():
    TransactionValidator.validate([])
