# Apache Kafka producer for sending messages to a Kafka topic
from confluent_kafka import Producer

producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'acks': 'all'
})

def produce_message(topic, data):
    # Serialize the data using Avro
    avro_data = serialize_data(data)

    # Produce the message to Kafka
    producer.produce(topic, value=avro_data)

    return producer.flush()

def serialize_data(data):
    # Serialize the data using Avro
    avro_schema = '''
        {
            "type": "record",
            "name": "MyData",
            "fields": [
                {"name": "field1", "type": "string"},
                {"name": "field2", "type": "int"}
            ]
        }
    '''
    avro_serializer = AvroSerializer(avro_schema)
    avro_data = avro_serializer.serialize(data)

    return avro_data
