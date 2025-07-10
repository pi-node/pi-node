import unittest
from unittest.mock import patch, MagicMock
from src.main import PiNode

class TestPiNode(unittest.TestCase):

    @patch('src.main.Node')
    @patch('src.main.API')
    @patch('src.main.Consensus')
    def setUp(self, MockConsensus, MockAPI, MockNode):
        """Set up the PiNode for testing with mocked components."""
        self.node = PiNode()
        self.node.node = MockNode.return_value
        self.node.api = MockAPI.return_value
        self.node.consensus = MockConsensus.return_value

    def test_initialization(self):
        """Test that the PiNode initializes correctly."""
        self.assertIsNotNone(self.node)
        self.assertIsNotNone(self.node.blockchain)
        self.assertIsNotNone(self.node.transaction_pool)
        self.assertIsNotNone(self.node.node)
        self.assertIsNotNone(self.node.api)
        self.assertIsNotNone(self.node.consensus)

    @patch('src.main.time.sleep', return_value=None)  # Mock sleep to avoid delays
    def test_start(self, mock_sleep):
        """Test the start method of PiNode."""
        with patch('src.main.logger') as mock_logger:
            self.node.start()
            mock_logger.info.assert_called_with("Starting Pi Node...")
            self.node.node.start.assert_called_once()
            self.node.api.start.assert_called_once()

    @patch('src.main.time.sleep', return_value=None)  # Mock sleep to avoid delays
    def test_run_consensus(self, mock_sleep):
        """Test the consensus running in the start method."""
        with patch('src.main.logger') as mock_logger:
            self.node.start()
            self.node.consensus.run.assert_called()

    @patch('src.main.logger')
    def test_graceful_shutdown(self, mock_logger):
        """Test that the node shuts down gracefully."""
        with patch('builtins.print') as mock_print:
            with patch('src.main.KeyboardInterrupt'):
                self.node.start()
                self.node.node.stop.assert_called_once()
                self.node.api.stop.assert_called_once()
                mock_logger.info.assert_called_with("Shutting down Pi Node...")

if __name__ == '__main__':
    unittest.main()
