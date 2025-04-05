import logging
import os
import json
from typing import Any, Dict

# Configure logging
def setup_logging(log_file: str = "app.log"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

# Custom Exception Class
class AppException(Exception):
    """Custom exception class for the application."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to a dictionary for JSON response."""
        return {"detail": self.message, "status_code": self.status_code}

# Configuration Management
def load_config(config_file: str = "config.json") -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    if not os.path.exists(config_file):
        raise AppException(f"Configuration file '{config_file}' not found.", status_code=404)

    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

# Input Validation
def validate_input(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Validate input data against required fields."""
    for field in required_fields:
        if field not in data:
            raise AppException(f"Missing required field: {field}", status_code=400)
        if not data[field]:
            raise AppException(f"Field '{field}' cannot be empty.", status_code=400)

# Example usage of logging and exception handling
if __name__ == "__main__":
    setup_logging()
    logging.info("Application started.")

    try:
        config = load_config()
        logging.info("Configuration loaded successfully.")
    except AppException as e:
        logging.error(f"Error loading configuration: {e.message}")
