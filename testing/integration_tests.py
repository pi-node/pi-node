# integration_tests.py
import unittest
from pi_supernode.security.access_control import AccessControl
from pi_supernode.data_analytics.data_ingestion import DataIngestion
from pi_supernode.data_analytics.data_processing import DataProcessing

class TestIntegration(unittest.TestCase):
    def test_access_control_integration(self):
        access_control = AccessControl()
        access_control.add_user('user1', ['read', 'write'])
        self.assertIn('user1', access_control.access_control)

    def test_data_ingestion_integration(self):
        data_ingestion = DataIngestion('topic', ['bootstrap_server'])
        data = data_ingestion.ingest_data()
        self.assertIsInstance(data, pd.DataFrame)

    def test_data_processing_integration(self):
        data_ingestion = DataIngestion('topic', ['bootstrap_server'])
        data = data_ingestion.ingest_data()
        data_processing = DataProcessing(data)
        processed_data = data_processing.preprocess_data()
        self.assertIsInstance(processed_data, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
