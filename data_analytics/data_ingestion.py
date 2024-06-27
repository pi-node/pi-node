# data_ingestion.py
import pandas as pd
import numpy as np
from kafka import KafkaConsumer
from typing import List, Dict

class DataIngestion:
    def __init__(self, kafka_topic: str, bootstrap_servers: List[str]):
        self.kafka_topic = kafka_topic
        self.bootstrap_servers = bootstrap_servers
        self.consumer = KafkaConsumer(self.kafka_topic, bootstrap_servers=self.bootstrap_servers)

    def ingest_data(self) -> pd.DataFrame:
        data = []
        for message in self.consumer:
            data.append(json.loads(message.value.decode('utf-8')))
        return pd.DataFrame(data)

    def ingest_realtime_data(self) -> None:
        for message in self.consumer:
            data = json.loads(message.value.decode('utf-8'))
            # Process real-time data here
            print(data)
