import json
from unittest.mock import MagicMock, patch, Mock
from src.kafka import fraud_detection_service_consume_produce

@patch("src.kafka.fraud_detection_service_consume_produce.Consumer")
def test_initiate_consumer(mock_consumer_class):
    mock_consumer = MagicMock()
    mock_consumer_class.return_value = mock_consumer

    consumer = fraud_detection_service_consume_produce.initiate_consumer()

    mock_consumer_class.assert_called_once_with({
        "bootstrap.servers": "localhost:9092",
        "group.id": "all-transactions",
        "auto.offset.reset": "earliest"
    })
    mock_consumer.subscribe.assert_called_once_with(
        topics=["transactions"]
    )
    assert consumer == mock_consumer

@patch("src.kafka.fraud_detection_service_consume_produce.Producer")
def test_initiate_producer(mock_producer_class):
    mock_producer = MagicMock()
    mock_producer_class.return_value = mock_producer

    producer = fraud_detection_service_consume_produce.initiate_producer()

    mock_producer_class.assert_called_once_with({
        "bootstrap.servers": "localhost:9092"
    })
    assert producer == mock_producer


def test_fetch_transaction_success():
    consumer = MagicMock()
    msg = MagicMock()

    msg.error.return_value = None
    msg.value.return_value = json.dumps({
        "transaction_id": "123",
        "amount": 50
    }).encode("utf-8")

    consumer.poll.return_value = msg

    transaction = fraud_detection_service_consume_produce.fetch_transaction(consumer)

    assert transaction["transaction_id"] == "123"
    assert transaction["amount"] == 50

def test_fetch_transaction_none():
    consumer = MagicMock()
    consumer.poll.return_value = None

    result = fraud_detection_service_consume_produce.fetch_transaction(consumer)

    assert result is None


def test_isFraud_detects_fraud():
    # GIVEN
    fraud_service = Mock()
    fraud_service.detect.return_value = ["tx-1"]

    transaction = {
        "transaction_id": "tx-1",
        "amount": 1000,
        "currency": "USD",
    }

    # WHEN
    alert = fraud_detection_service_consume_produce.isFraud(
        transaction,
        fraud_service
    )

    # THEN
    assert alert["fraud"] is True
    assert alert["transaction_id"] == "tx-1"

    fraud_service.detect.assert_called_once_with([transaction])

def test_isFraud_no_fraud():
    # GIVEN
    fraud_service = Mock()
    fraud_service.detect.return_value = []

    transaction = {
        "transaction_id": "tx-2",
        "amount": 50,
        "currency": "USD",
    }

    # WHEN
    alert = fraud_detection_service_consume_produce.isFraud(
        transaction,
        fraud_service
    )

    # THEN
    assert alert["fraud"] is False
    assert alert["transaction_id"] == "tx-2"

    fraud_service.detect.assert_called_once_with([transaction])

def test_isAlert_true():
    assert fraud_detection_service_consume_produce.isAlert({"fraud": True}) is True

def test_isAlert_false():
    assert fraud_detection_service_consume_produce.isAlert({"fraud": False}) is False

@patch("src.kafka.fraud_detection_service_consume_produce.uuid.uuid4")
def test_generateAlert(mock_uuid):
    mock_uuid.return_value = "abc-123"

    response = {"transaction_id": "tx-9"}
    result = fraud_detection_service_consume_produce.generateAlert(response)

    decoded = json.loads(result.decode("utf-8"))

    assert decoded["transaction_id"] == "tx-9"
    assert decoded["alert_id"] == "alert-abc-123"

def test_sendAlert():
    producer = MagicMock()
    alert = b"alert-data"

    fraud_detection_service_consume_produce.sendAlert(producer, alert)

    producer.produce.assert_called_once_with(
        topic="alerts",
        value=alert,
        callback=fraud_detection_service_consume_produce.delivery_report
    )
    producer.flush.assert_called_once()


