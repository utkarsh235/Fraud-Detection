import pandas as pd
from src.naive_fraud_detection.fraud_detection import FraudDetection
from src.dataclass.transaction import Transaction

def test_fraud_detection_flags_invalid_transactions():
    df = pd.DataFrame([
        {"transaction_id": "tx-1", "amount": -5},
        {"transaction_id": "tx-2", "amount": 50},
        {"transaction_id": "tx-3", "amount": 0},
    ])

    detector = FraudDetection(method="naive", data=df)
    detector.check()

    assert detector.get_flagged_transactions() == ["tx-1", "tx-3"]

def test_fraud_detection_no_fraud_found():
    df = pd.DataFrame([
        {"transaction_id": "tx-10", "amount": 10},
        {"transaction_id": "tx-11", "amount": 20},
    ])

    detector = FraudDetection(method="naive", data=df)
    detector.check()

    assert detector.get_flagged_transactions() == []

def test_fraud_detection_non_naive_method_does_nothing():
    df = pd.DataFrame([
        {"transaction_id": "tx-1", "amount": -100},
    ])

    detector = FraudDetection(method="ml", data=df)
    detector.check()

    assert detector.get_flagged_transactions() == []
