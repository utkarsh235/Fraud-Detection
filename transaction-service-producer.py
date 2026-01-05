from confluent_kafka import Producer
import uuid
import json

def initiate_producer():
    producer_config = {
        'bootstrap.servers': 'localhost:9092'
    }
    producer = Producer(producer_config)
    return producer

def delivery_report(err, msg):
    if err: 
        print('Delivery Report ERROR! -> ', err)
    else: 
        print("Delivery SUCCEEDED! -> ", {msg.value().decode('utf-8')})

def get_transaction():
    transaction = {
        'transaction_id': str(uuid.uuid4()),
        'amount': -500,
        'currency': 'CHZ'
    }

    return json.dumps(transaction).encode('utf-8')

def main():
    producer = initiate_producer()
    for _ in range(3):
        transaction = get_transaction()
        producer.produce(
            topic='transactions',
            value=transaction,
            callback=delivery_report
        )
    producer.flush()

if __name__=="__main__":
    main()