import json
from unittest.mock import MagicMock, patch
import pytest
from src.kafka import alerts_service_consumer

@patch("src.kafka.alerts_service_consumer.Consumer")
def test_initiate_consumer(mock_consumer_class):
    mock_consumer = MagicMock()
    mock_consumer_class.return_value = mock_consumer

    consumer = alerts_service_consumer.initiate_consumer()

    mock_consumer_class.assert_called_once_with({
        "bootstrap.servers": "localhost:9092",
        "group.id": "alerts",
        "auto.offset.reset": "earliest",
    })

    mock_consumer.subscribe.assert_called_once_with(
        topics=["alerts"]
    )

    assert consumer == mock_consumer

@pytest.mark.skip()
def test_call_consumer_processes_message_and_closes():
    consumer = MagicMock()
    msg = MagicMock()

    msg.error.return_value = None
    msg.value.return_value = json.dumps({
        "transaction_id": "tx-1",
        "alert_id": "alert-123"
    }).encode("utf-8")

    # First poll returns message, second raises exception to break loop
    consumer.poll.side_effect = [
        msg,
        KeyboardInterrupt()
    ]

    alerts_service_consumer.call_consumer(consumer)

    consumer.close.assert_called_once()

@pytest.mark.skip()
def test_call_consumer_message_error():
    consumer = MagicMock()
    msg = MagicMock()

    msg.error.return_value = Exception("Kafka error")

    consumer.poll.side_effect = [
        msg,
        KeyboardInterrupt()
    ]

    alerts_service_consumer.call_consumer(consumer)

    consumer.close.assert_called_once()

@pytest.mark.skip()
def test_call_consumer_poll_none():
    consumer = MagicMock()

    consumer.poll.side_effect = [
        None,
        KeyboardInterrupt()
    ]

    alerts_service_consumer.call_consumer(consumer)

    consumer.close.assert_called_once()
