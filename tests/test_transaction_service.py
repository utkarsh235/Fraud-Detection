from src.kafka import transaction_service_producer
import json
from unittest.mock import MagicMock, patch

@patch("src.kafka.transaction_service_producer.Producer")
def test_initiate_producer(mock_producer_class):
    mock_instance = MagicMock()
    mock_producer_class.return_value = mock_instance

    producer = transaction_service_producer.initiate_producer()

    mock_producer_class.assert_called_once_with({
        "bootstrap.servers": "localhost:9092"
    })
    assert producer == mock_instance

def test_delivery_report_success(capsys):
    mock_msg = MagicMock()
    mock_msg.value.return_value = b'{"status":"ok"}'

    transaction_service_producer.delivery_report(None, mock_msg)

    captured = capsys.readouterr()
    assert "Delivery SUCCEEDED!" in captured.out

def test_delivery_report_error(capsys):
    error = Exception("Kafka error")

    transaction_service_producer.delivery_report(error, None)

    captured = capsys.readouterr()
    assert "Delivery Report ERROR!" in captured.out

@patch("src.kafka.transaction_service_producer.uuid.uuid4")
def test_get_transaction(mock_uuid):
    mock_uuid.return_value = "1234"

    result = transaction_service_producer.get_transaction()

    assert isinstance(result, bytes)

    decoded = json.loads(result.decode("utf-8"))

    assert decoded["transaction_id"] == "1234"
    assert decoded["amount"] == 10
    assert decoded["currency"] == "USD"

@patch("src.kafka.transaction_service_producer.initiate_producer")
def test_main_produces_three_messages(mock_initiate):
    mock_producer = MagicMock()
    mock_initiate.return_value = mock_producer

    transaction_service_producer.main()

    # produce called exactly 3 times
    assert mock_producer.produce.call_count == 3

    for call in mock_producer.produce.call_args_list:
        kwargs = call.kwargs
        assert kwargs["topic"] == "transactions"
        assert kwargs["callback"] == transaction_service_producer.delivery_report
        assert isinstance(kwargs["value"], bytes)

    mock_producer.flush.assert_called_once()
