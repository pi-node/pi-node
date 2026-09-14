import pytest
import os
import json
import logging
from src.utils import setup_logging, AppException, load_config, validate_input

# Test logging setup
def test_setup_logging(caplog):
    """Test logging setup."""
    setup_logging("test.log")
    logging.info("Test log message.")
    
    # Check if the log message is captured
    assert "Test log message." in caplog.text

# Test AppException
def test_app_exception():
    """Test the AppException class."""
    exception = AppException("This is a test error", status_code=400)
    assert exception.message == "This is a test error"
    assert exception.status_code == 400
    assert exception.to_dict() == {"detail": "This is a test error", "status_code": 400}

# Test load_config with a valid file
def test_load_config_valid():
    """Test loading configuration from a valid JSON file."""
    config_data = {
        "key1": "value1",
        "key2": "value2"
    }
    with open("test_config.json", "w") as f:
        json.dump(config_data, f)

    config = load_config("test_config.json")
    assert config == config_data

    # Clean up
    os.remove("test_config.json")

# Test load_config with a missing file
def test_load_config_missing_file():
    """Test loading configuration from a missing file."""
    with pytest.raises(AppException) as excinfo:
        load_config("missing_config.json")
    assert excinfo.value.message == "Configuration file 'missing_config.json' not found."
    assert excinfo.value.status_code == 404

# Test validate_input with valid data
def test_validate_input_valid():
    """Test input validation with valid data."""
    data = {"field1": "value1", "field2": "value2"}
    required_fields = ["field1", "field2"]
    
    try:
        validate_input(data, required_fields)
    except AppException:
        pytest.fail("validate_input raised AppException unexpectedly!")

# Test validate_input with missing fields
def test_validate_input_missing_field():
    """Test input validation with missing required fields."""
    data = {"field1": "value1"}
    required_fields = ["field1", "field2"]
    
    with pytest.raises(AppException) as excinfo:
        validate_input(data, required_fields)
    assert excinfo.value.message == "Missing required field: field2"
    assert excinfo.value.status_code == 400

# Test validate_input with empty fields
def test_validate_input_empty_field():
    """Test input validation with empty required fields."""
    data = {"field1": "", "field2": "value2"}
    required_fields = ["field1", "field2"]
    
    with pytest.raises(AppException) as excinfo:
        validate_input(data, required_fields)
    assert excinfo.value.message == "Field 'field1' cannot be empty."
    assert excinfo.value.status_code == 400

if __name__ == "__main__":
    pytest.main()
