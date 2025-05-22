
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from customer_generator import CustomerGenerator

# Define the Avro schema for customer data
customer_schema_str = '''
{
    "type": "record",
    "name": "Customer",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "email", "type": "string"},
        {"name": "address", "type": "string"},
        {"name": "phone_number", "type": "string"},
        {"name": "birthdate", "type": "string"}
    ]
}
'''

# Configuration for Schema Registry
schema_registry_conf = {
    'url': 'http://10.222.68.223:8081'  # Replace with your Schema Registry URL
}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Avro serializer for customer data
avro_serializer = AvroSerializer(
    schema_registry_client,
    customer_schema_str,
    to_dict=lambda obj, ctx: obj  # Assuming the customer data is already in dictionary format
)

# Configuration for Kafka producer
producer_conf = {
    'bootstrap.servers': '10.222.68.223:9092',  # Replace with your Kafka broker URL
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer
}

producer = SerializingProducer(producer_conf)

# Function to produce customer data to Kafka
def produce_customer_data():
    customer_generator = CustomerGenerator()
    customer_data = customer_generator.generate_customer()
    producer.produce(topic='customer_topic', key=customer_data['email'], value=customer_data)
    producer.flush()

if __name__ == '__main__':
    produce_customer_data()
