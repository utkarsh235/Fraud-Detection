from confluent_kafka import Consumer
import json

def initiate_consumer():
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "alerts",
        "auto.offset.reset": "earliest"
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe(topics=["alerts"])
    print("Consumer is Running and Subscribed to alerts topic...")

    return consumer

def call_consumer(consumer):
    try: 
        while True:
            msg = consumer.poll(1.0)
            if msg is None: 
                continue
            if msg.error():
                print("ERROR when reading message -> ", msg.error())
                continue

            value = msg.value().decode("utf-8")
            alert = json.loads(value)
            print("New message RECEIVED: -> ", alert)

    except Exception as e: 
        print(e)
    finally: 
        consumer.close()

def main():
    consumer = initiate_consumer()
    call_consumer(consumer)

if __name__ == "__main__":
    main()