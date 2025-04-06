# config.py

import os
import json
import logging
from datetime import datetime

# Load environment variables for sensitive data
from dotenv import load_dotenv
load_dotenv()

# Configuration for Pi Supernode

# Coin symbol and name
COIN_SYMBOL = os.getenv("COIN_SYMBOL", "Pi")
COIN_NAME = os.getenv("COIN_NAME", "Pi Coin")

# Stablecoin value in USD
STABLECOIN_VALUE = float(os.getenv("STABLECOIN_VALUE", 314159.00))

# Network settings
NETWORK_ID = os.getenv("NETWORK_ID", "mainnet")  # Change to "testnet" if needed
RPC_PORT = int(os.getenv("RPC_PORT", 51473))
API_PORT = int(os.getenv("API_PORT", 51474))

# Node settings
NODE_IP = os.getenv("NODE_IP", "0.0.0.0")  # Listen on all interfaces
NODE_PORT = int(os.getenv("NODE_PORT", 51475))

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = os.getenv("LOG_FILE", "pi_supernode.log")

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pi_supernode.db")  # Change to your preferred database

# Security settings
ENABLE_SSL = bool(int(os.getenv("ENABLE_SSL", 1)))  # Set to 1 to enable SSL
SSL_CERT_PATH = os.getenv("SSL_CERT_PATH", "/path/to/your/cert.pem")  # Path to SSL certificate
SSL_KEY_PATH = os.getenv("SSL_KEY_PATH", "/path/to/your/key.pem")  # Path to SSL key

# API Integration
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://api.example.com/data")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))  # Timeout for API requests in seconds

# Advanced logging configuration
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Dynamic configuration loading
def load_dynamic_config():
    try:
        with open('dynamic_config.json', 'r') as f:
            dynamic_config = json.load(f)
            return dynamic_config
    except FileNotFoundError:
        logging.warning("Dynamic configuration file not found. Using default settings.")
        return {}

# Load dynamic configurations
DYNAMIC_CONFIG = load_dynamic_config()

# Additional settings can be added as needed
# Example: Custom transaction fees
TRANSACTION_FEE = DYNAMIC_CONFIG.get("TRANSACTION_FEE", 0.01)  # Default fee

# Example: Enable/disable features
ENABLE_FEATURE_X = DYNAMIC_CONFIG.get("ENABLE_FEATURE_X", True)

# Print configuration for debugging
def print_config():
    logging.info("Current Configuration:")
    logging.info(f"COIN_SYMBOL: {COIN_SYMBOL}")
    logging.info(f"COIN_NAME: {COIN_NAME}")
    logging.info(f"STABLECOIN_VALUE: {STABLECOIN_VALUE}")
    logging.info(f"NETWORK_ID: {NETWORK_ID}")
    logging.info(f"RPC_PORT: {RPC_PORT}")
    logging.info(f"API_PORT: {API_PORT}")
    logging.info(f"NODE_IP: {NODE_IP}")
    logging.info(f"NODE_PORT: {NODE_PORT}")
    logging.info(f"LOG_LEVEL: {LOG_LEVEL}")
    logging.info(f"DATABASE_URL: {DATABASE_URL}")
    logging.info(f"ENABLE_SSL: {ENABLE_SSL}")
    logging.info(f"EXTERNAL_API_URL: {EXTERNAL_API_URL}")
    logging.info(f"TRANSACTION_FEE: {TRANSACTION_FEE}")
    logging.info(f"ENABLE_FEATURE_X: {ENABLE_FEATURE_X}")

# Call to print the configuration
print_config()
