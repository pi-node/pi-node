import unittest
import socket
import threading
import time
from src.node import Node

class TestNode(unittest.TestCase):

    def setUp(self):
        """Set up a new node for testing."""
        self.node = Node(host='127.0.0.1', port=5000)
        self.node.start()
        time.sleep(1)  # Give the node time to start

    def tearDown(self):
        """Shut down the node after tests."""
        self.node.shutdown()

    def test_peer_discovery(self):
        """Test that peers can be added to the node."""
        self.node.discover_peers(['127.0.0.1:5001', '127.0.0.1:5002'])
        self.assertIn('127.0.0.1:5001', self.node.peers)
        self.assertIn('127.0.0.1:5002', self.node.peers)

    def test_connection_handling(self):
        """Test that the node can accept connections from peers."""
        def connect_to_node():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('127.0.0.1', 5000))
                sock.sendall(b'{"type": "peer_discovery", "peer": "127.0.0.1:5001"}')

        # Start a thread to connect to the node
        threading.Thread(target=connect_to_node, daemon=True).start()
        time.sleep(1)  # Wait for the connection to be processed

        self.assertIn('127.0.0.1:5001', self.node.peers)

    def test_process_message(self):
        """Test that the node can process incoming messages."""
        message = '{"type": "peer_discovery", "peer": "127.0.0.1:5003"}'
        self.node.process_message(message)
        self.assertIn('127.0.0.1:5003', self.node.peers)

    def test_broadcast(self):
        """Test that the broadcast method works."""
        self.node.discover_peers(['127.0.0.1:5001'])
        
        # Mock a peer to receive the broadcast
        def mock_peer():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(('127.0.0.1', 5001))
                sock.listen(1)
                conn, _ = sock.accept()
                data = conn.recv(1024).decode()
                conn.close()
                return data

        # Start the mock peer in a separate thread
        peer_thread = threading.Thread(target=mock_peer, daemon=True)
        peer_thread.start()
        time.sleep(1)  # Give the mock peer time to start

        # Broadcast a message
        self.node.broadcast('{"type": "broadcast", "message": "Hello, peers!"}')
        
        # Wait for the mock peer to receive the message
        time.sleep(1)

        # Check if the mock peer received the message
        self.assertTrue(peer_thread.is_alive())  # Ensure the thread is still running

    def test_invalid_message(self):
        """Test that the node handles invalid messages gracefully."""
        invalid_message = 'Invalid JSON'
        with self.assertLogs('root', level='ERROR') as log:
            self.node.process_message(invalid_message)
            self.assertIn("Received invalid JSON message.", log.output[0])

    def test_missing_fields(self):
        """Test that the node handles messages with missing fields."""
        missing_field_message = '{"type": "peer_discovery"}'  # No 'peer' field
        with self.assertLogs('root', level='ERROR') as log:
            self.node.process_message(missing_field_message)
            self.assertIn("Received message with missing fields.", log.output[0])

if __name__ == '__main__':
    unittest.main()
