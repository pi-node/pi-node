import unittest
import requests
import logging

# Configure logging
logging.basicConfig(filename='integration_tests.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestPiSupernodeIntegration(unittest.TestCase):
    BASE_URL = "http://localhost:3000"  # Update this to your application's base URL

    @classmethod
    def setUpClass(cls):
        """Set up any state specific to the test class."""
        logging.info("Setting up integration tests.")

    @classmethod
    def tearDownClass(cls):
        """Clean up any state specific to the test class."""
        logging.info("Tearing down integration tests.")

    def test_health_check(self):
        """Test the health check endpoint."""
        logging.info("Testing health check endpoint.")
        response = requests.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'ok')

    def test_data_endpoint(self):
        """Test the data retrieval endpoint."""
        logging.info("Testing data retrieval endpoint.")
        response = requests.get(f"{self.BASE_URL}/data")
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())

    def test_post_data(self):
        """Test posting data to the application."""
        logging.info("Testing posting data to the application.")
        payload = {'key': 'value'}
        response = requests.post(f"{self.BASE_URL}/data", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('message'), 'Data created successfully.')

    def test_invalid_endpoint(self):
        """Test an invalid endpoint."""
        logging.info("Testing an invalid endpoint.")
        response = requests.get(f"{self.BASE_URL}/invalid")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    logging.info("Starting integration tests.")
    unittest.main()
