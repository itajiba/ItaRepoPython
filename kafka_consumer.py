from confluent_kafka import Consumer, KafkaException

# Kafka configuration
conf = {
    'bootstrap.servers': '10.222.68.223:9092',
    'group.id': 'customer-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Create Consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
topic = 'customer_topic'  # Make sure this matches your producer's topic
consumer.subscribe([topic])

print(f"Subscribed to topic: {topic}")
print("Waiting for messages... Press Ctrl+C to stop.")

try:
    while True:
        msg = consumer.poll(1.0)  # Wait for message or timeout
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("Consumer stopped manually.")

finally:
    consumer.close()