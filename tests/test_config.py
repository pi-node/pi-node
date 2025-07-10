import unittest
import os
from unittest.mock import patch
from src.config import Config

class TestConfig(unittest.TestCase):

    @patch.dict(os.environ, {}, clear=True)  # Clear environment variables for testing
    def test_default_values(self):
        """Test that default configuration values are set correctly."""
        config = Config()
        self.assertEqual(config.NETWORK_NAME, "PiNetwork")
        self.assertEqual(config.NETWORK_PORT, 5000)
        self.assertEqual(config.NETWORK_HOST, "0.0.0.0")
        self.assertEqual(config.MAX_CONNECTIONS, 100)
        self.assertEqual(config.BLOCK_TIME, 10)
        self.assertEqual(config.DIFFICULTY, 2)
        self.assertEqual(config.API_VERSION, "v1")
        self.assertEqual(config.CONSENSUS_INTERVAL, 15)
        self.assertEqual(config.LOG_LEVEL, "INFO")
        self.assertEqual(config.DATABASE_URL, "sqlite:///pi_network.db")
        self.assertFalse(config.ENABLE_SSL)
        self.assertFalse(config.MAINTENANCE_MODE)

    @patch.dict(os.environ, {
        "NETWORK_NAME": "TestNetwork",
        "NETWORK_PORT": "8080",
        "NETWORK_HOST": "127.0.0.1",
        "MAX_CONNECTIONS": "200",
        "BLOCK_TIME": "5",
        "DIFFICULTY": "3",
        "API_VERSION": "v2",
        "CONSENSUS_INTERVAL": "10",
        "LOG_LEVEL": "DEBUG",
        "DATABASE_URL": "postgresql://user:password@localhost/dbname",
        "ENABLE_SSL": "1",
        "MAINTENANCE_MODE": "1"
    })
    def test_environment_variables(self):
        """Test that configuration values are loaded from environment variables."""
        config = Config()
        self.assertEqual(config.NETWORK_NAME, "TestNetwork")
        self.assertEqual(config.NETWORK_PORT, 8080)
        self.assertEqual(config.NETWORK_HOST, "127.0.0.1")
        self.assertEqual(config.MAX_CONNECTIONS, 200)
        self.assertEqual(config.BLOCK_TIME, 5)
        self.assertEqual(config.DIFFICULTY, 3)
        self.assertEqual(config.API_VERSION, "v2")
        self.assertEqual(config.CONSENSUS_INTERVAL, 10)
        self.assertEqual(config.LOG_LEVEL, "DEBUG")
        self.assertEqual(config.DATABASE_URL, "postgresql://user:password@localhost/dbname")
        self.assertTrue(config.ENABLE_SSL)
        self.assertTrue(config.MAINTENANCE_MODE)

    def test_display_config(self):
        """Test that the display_config method works without errors."""
        with patch('builtins.print') as mock_print:
            config = Config()
            config.display_config()
            self.assertTrue(mock_print.called)  # Ensure print was called

if __name__ == '__main__':
    unittest.main()
