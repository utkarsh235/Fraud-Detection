import json
import os
import tempfile

import pytest

from src.service.fraud_service import FraudService
from src.domain.transaction import Transaction


@pytest.fixture
def temp_repository_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield os.path.join(tmpdir, "transactions.csv")


@pytest.fixture
def valid_transactions():
    return [
        Transaction(
            transaction_id="t1",
            amount=50,
            currency="USD"
        ),
        Transaction(
            transaction_id="t2",
            amount=100000, 
            currency="USD"
        ),
        Transaction(
            transaction_id="t3",
            amount=100000,
            currency="USD"
        ),
        Transaction(
            transaction_id="t4",
            amount=100000,
            currency="USD"
        ),
    ]


def test_fraud_service_end_to_end(temp_repository_path, valid_transactions):
    # GIVEN
    service = FraudService(transaction_path=temp_repository_path)

    # WHEN
    flagged = service.detect(valid_transactions)

    # THEN
    assert flagged is not None

    assert len(flagged) == 1
    assert "t1" in flagged


