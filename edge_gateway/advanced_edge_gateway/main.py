# edge_gateway/main.py
import os
import json
from kafka import KafkaDataProcessor
from anomaly_detection import AnomalyDetector
from secure_communication import MutualTLS

class EdgeGateway:
    def __init__(self, config_file='config.json'):
        self.config = EdgeGatewayConfig(config_file)
        self.kafka_processor = KafkaDataProcessor(**self.config.get_kafka_config())
        self.anomaly_detector = AnomalyDetector(**self.config.get_anomaly_detection_config())
        self.mutual_tls = MutualTLS(**self.config.get_mutual_tls_config())

    def start(self):
        # Start consuming from Kafka topic
        self.kafka_processor.startConsuming()

        # Start anomaly detection
        self.anomaly_detector.train_model([])  # Train the model with some data

        # Establish secure connection using mutual TLS
        self.mutual_tls.connect("example.com", 443)

        # Send and receive data over the secure connection
        self.mutual_tls.send_data("Hello, server!")
        buffer = bytearray(1024)
        self.mutual_tls.receive_data(buffer, 1024)
        print(buffer.decode())

if __name__ == "__main__":
    edge_gateway = EdgeGateway()
    edge_gateway.start()
