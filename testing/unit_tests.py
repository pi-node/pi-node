# unit_tests.py
import unittest
from unittest.mock import patch, MagicMock
from pi_supernode.security.access_control import AccessControl
from pi_supernode.data_analytics.data_ingestion import DataIngestion

class TestAccessControl(unittest.TestCase):
    def test_add_user(self):
        access_control = AccessControl()
        access_control.add_user('user1', ['read', 'write'])
        self.assertIn('user1', access_control.access_control)

    def test_check_permission(self):
        access_control = AccessControl()
        access_control.add_user('user1', ['read', 'write'])
        self.assertTrue(access_control.check_permission('user1', 'read'))

class TestDataIngestion(unittest.TestCase):
    @patch('kafka.KafkaConsumer')
    def test_ingest_data(self, mock_kafka_consumer):
        mock_kafka_consumer.return_value = MagicMock()
        data_ingestion = DataIngestion('topic', ['bootstrap_server'])
        data = data_ingestion.ingest_data()
        self.assertIsInstance(data, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
