import socket
import threading
import json
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Node:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: List[str] = []  # List of peer nodes
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        logging.info(f"Node started at {self.host}:{self.port}")

    def start(self):
        """Start the node and listen for incoming connections."""
        threading.Thread(target=self.accept_connections, daemon=True).start()
        logging.info("Node is listening for connections...")

    def accept_connections(self):
        """Accept incoming connections from peers."""
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                logging.info(f"Connection from {address} has been established.")
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except Exception as e:
                logging.error(f"Error accepting connections: {e}")

    def handle_client(self, client_socket: socket.socket):
        """Handle communication with a connected peer."""
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.process_message(message)
            except Exception as e:
                logging.error(f"Error handling client: {e}")
                break
        client_socket.close()

    def process_message(self, message: str):
        """Process incoming messages from peers."""
        try:
            data = json.loads(message)
            if data['type'] == 'peer_discovery':
                self.add_peer(data['peer'])
            elif data['type'] == 'transaction':
                self.handle_transaction(data['transaction'])
            elif data['type'] == 'broadcast':
                self.handle_broadcast(data['message'])
        except json.JSONDecodeError:
            logging.error("Received invalid JSON message.")
        except KeyError:
            logging.error("Received message with missing fields.")

    def add_peer(self, peer: str):
        """Add a new peer to the list of peers."""
        if peer not in self.peers:
            self.peers.append(peer)
            logging.info(f"Added new peer: {peer}")

    def handle_transaction(self, transaction: Dict[str, Any]):
        """Handle a new transaction received from a peer."""
        logging.info(f"Received transaction: {transaction}")
        # Here you would typically validate and add the transaction to the pool

    def handle_broadcast(self, message: str):
        """Handle a broadcast message from a peer."""
        logging.info(f"Broadcast message received: {message}")

    def broadcast(self, message: str):
        """Broadcast a message to all connected peers."""
        for peer in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((peer.split(':')[0], int(peer.split(':')[1])))
                    sock.sendall(message.encode())
                    logging.info(f"Broadcasted message to {peer}")
            except Exception as e:
                logging.error(f"Could not send message to {peer}: {e}")

    def discover_peers(self, peer_list: List[str]):
        """Discover and add peers from a given list."""
        for peer in peer_list:
            self.add_peer(peer)

    def shutdown(self):
        """Gracefully shut down the node."""
        logging.info("Shutting down the node...")
        self.server_socket.close()

# Example usage
if __name__ == "__main__":
    node = Node(host='127.0.0.1', port=5000)
    node.start()

    # Simulate peer discovery
    node.discover_peers(['127.0.0.1:5001', '127.0.0.1:5002'])

    try:
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        node.shutdown()
