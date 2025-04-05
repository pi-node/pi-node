import os

class Config:
    # Network settings
    NETWORK_NAME = os.getenv("NETWORK_NAME", "PiNetwork")
    NETWORK_PORT = int(os.getenv("NETWORK_PORT", 5000))
    NETWORK_HOST = os.getenv("NETWORK_HOST", "0.0.0.0")
    MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", 100))

    # Blockchain settings
    BLOCK_TIME = int(os.getenv("BLOCK_TIME", 10))  # Time in seconds to create a new block
    DIFFICULTY = int(os.getenv("DIFFICULTY", 2))    # Difficulty level for mining

    # API settings
    API_VERSION = os.getenv("API_VERSION", "v1")
    API_ENDPOINT = os.getenv("API_ENDPOINT", f"http://{NETWORK_HOST}:{NETWORK_PORT}/api/{API_VERSION}")

    # Consensus settings
    CONSENSUS_INTERVAL = int(os.getenv("CONSENSUS_INTERVAL", 15))  # Time in seconds between consensus rounds

    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pi_network.db")  # Default to SQLite

    # Security settings
    ENABLE_SSL = bool(os.getenv("ENABLE_SSL", False))  # Enable SSL for API
    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH", "path/to/cert.pem")
    SSL_KEY_PATH = os.getenv("SSL_KEY_PATH", "path/to/key.pem")

    # Other settings
    MAINTENANCE_MODE = bool(os.getenv("MAINTENANCE_MODE", False))  # Enable maintenance mode

    @classmethod
    def display_config(cls):
        """Display the current configuration settings."""
        print("Current Configuration:")
        print(f"Network Name: {cls.NETWORK_NAME}")
        print(f"Network Host: {cls.NETWORK_HOST}")
        print(f"Network Port: {cls.NETWORK_PORT}")
        print(f"Max Connections: {cls.MAX_CONNECTIONS}")
        print(f"Block Time: {cls.BLOCK_TIME} seconds")
        print(f"Difficulty: {cls.DIFFICULTY}")
        print(f"API Endpoint: {cls.API_ENDPOINT}")
        print(f"Consensus Interval: {cls.CONSENSUS_INTERVAL} seconds")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"Database URL: {cls.DATABASE_URL}")
        print(f"SSL Enabled: {cls.ENABLE_SSL}")
        print(f"Maintenance Mode: {cls.MAINTENANCE_MODE}")

# Example usage
if __name__ == "__main__":
    Config.display_config()
