from confluent_kafka import Consumer, Producer
import json
import uuid
from src.service.fraud_service import FraudService

def initiate_consumer():
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "all-transactions",
        "auto.offset.reset": "earliest"
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe(topics=["transactions"])
    print("Consumer is Running and Subscribed to transactions topic...")
    return consumer

def initiate_producer():
    producer_config = {
        "bootstrap.servers": "localhost:9092",
    }
    producer = Producer(producer_config)
    return producer

def initiate_fraud_detection_service():
    service = FraudService('src/datasets/transactions.csv')
    return service

def delivery_report(err, msg):
    if err: 
        print('Delivery Report ERROR! -> ', err)
    else: 
        print("Delivery SUCCEEDED! -> ", {msg.value().decode('utf-8')})

def fetch_transaction(consumer):
    msg = consumer.poll(1.0)
    if msg is None: 
        return None
    if msg.error():
        print("ERROR when reading message -> ", msg.error())

    value = msg.value().decode("utf-8")
    transaction = json.loads(value)
    print("New message RECEIVED: -> ", transaction)
    return transaction

def isFraud(transaction, fraud_service): 
    alert = {
        'transaction_id': transaction['transaction_id'],
        'fraud': False
    }
    fraud_ids = fraud_service.detect([transaction])
    if (fraud_ids):
        transaction_id = fraud_ids[0]
        alert["transaction_id"] = transaction_id
        alert['fraud'] = True

    return alert 

def isAlert(response):
    if response['fraud']:
        return True
    return False

def generateAlert(response):
    alert = {
        'transaction_id': response['transaction_id'], 
        'alert_id': "alert-" + str(uuid.uuid4())
    }
    return json.dumps(alert).encode('utf-8')

def sendAlert(producer, alert):
    producer.produce(
        topic='alerts',
        value=alert,
        callback=delivery_report
    )
    producer.flush()

def main():
    consumer = initiate_consumer()
    producer = initiate_producer()
    fraud_service = initiate_fraud_detection_service()
    try: 
        while True: 
            transaction = fetch_transaction(consumer)
            if transaction:
                response = isFraud(transaction=transaction, fraud_service=fraud_service)
                if isAlert(response):
                    alert = generateAlert(response)
                    sendAlert(producer, alert)

    except Exception as e:
        print(e) 
        print("Connection interupted")

    finally: 
        consumer.close()

if __name__=="__main__":
    main()