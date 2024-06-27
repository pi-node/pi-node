# edge_gateway/config.py
import os
import json
from cryptography.fernet import Fernet

class EdgeGatewayConfig:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

        # Load encryption key from environment variable
        self.encryption_key = os.environ.get('EDGE_GATEWAY_ENC_KEY')
        self.fernet = Fernet(self.encryption_key.encode())

    def get_device_list(self):
        return self.config.get('devices', [])

    def get_device_config(self, device_id):
        return self.config.get('devices', {}).get(device_id, {})

    def encrypt_data(self, data):
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data.encode()).decode()

    def get_kafka_config(self):
        return self.config.get('kafka', {})

    def get_anomaly_detection_config(self):
        return self.config.get('anomaly_detection', {})

    def get_mutual_tls_config(self):
        return self.config.get('mutual_tls', {})
