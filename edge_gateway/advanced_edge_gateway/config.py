import logging
import os
import json
import yaml
import cryptography
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(filename='config.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConfigManager:
    def __init__(self, config_file='config.json', encryption_key_file='encryption_key.key'):
        self.config_file = config_file
        self.encryption_key_file = encryption_key_file
        self.config = self.load_config()
        self.encryption_key = self.load_encryption_key()

    def load_config(self):
        """Load configuration from a JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                logging.info("Configuration loaded successfully.")
                return config
        else:
            logging.error(f"Configuration file {self.config_file} not found. Using default settings.")
            return {}

    def load_encryption_key(self):
        """Load encryption key from a file."""
        if os.path.exists(self.encryption_key_file):
            with open(self.encryption_key_file, 'rb') as file:
                encryption_key = file.read()
                logging.info("Encryption key loaded successfully.")
                return encryption_key
        else:
            logging.error(f"Encryption key file {self.encryption_key_file} not found. Generating a new key.")
            encryption_key = Fernet.generate_key()
            with open(self.encryption_key_file, 'wb') as file:
                file.write(encryption_key)
            return encryption_key

    def validate_config(self):
        """Validate configuration settings."""
        required_settings = ['registry_uri', 'monitor_uri', 'sensor_device_path']
        for setting in required_settings:
            if setting not in self.config:
                logging.error(f"Missing required setting: {setting}")
                return False
        return True

    def encrypt_config(self):
        """Encrypt configuration settings."""
        fernet = Fernet(self.encryption_key)
        encrypted_config = fernet.encrypt(json.dumps(self.config).encode())
        with open(self.config_file, 'wb') as file:
            file.write(encrypted_config)
        logging.info("Configuration encrypted successfully.")

    def decrypt_config(self):
        """Decrypt configuration settings."""
        fernet = Fernet(self.encryption_key)
        with open(self.config_file, 'rb') as file:
            encrypted_config = file.read()
        decrypted_config = fernet.decrypt(encrypted_config).decode()
        self.config = json.loads(decrypted_config)
        logging.info("Configuration decrypted successfully.")

    def save_config(self):
        """Save configuration settings to a file."""
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file)
        logging.info("Configuration saved successfully.")

    def load_yaml_config(self, yaml_file):
        """Load configuration from a YAML file."""
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)
            logging.info("YAML configuration loaded successfully.")
            return config

if __name__ == "__main__":
    config_manager = ConfigManager()
    if config_manager.validate_config():
        config_manager.encrypt_config()
    else:
        logging.error("Invalid configuration settings.")
