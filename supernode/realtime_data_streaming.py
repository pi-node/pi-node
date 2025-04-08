# realtime_data_streaming.py
from confluent_kafka import Producer

class DataStreamingProducer:
    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': 'localhost:9092',
            'client.id': 'pi-supernode-producer'
        })

    def send_message(self, topic, message):
        # Send a message to a Kafka topic
        self.producer.produce(topic=topic, value=message)
        self.producer.flush()

# Example usage:
data_streaming_producer = DataStreamingProducer()
data_streaming_producer.send_message("pi-supernode-data", "Temperature: 25.3°C")
