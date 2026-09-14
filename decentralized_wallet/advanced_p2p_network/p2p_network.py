# Advanced P2P network functionality
import socket
from cryptography.hazmat.primitives import serialization

class P2PNetwork:
    def __init__(self, blockchain_manager):
        self.blockchain_manager = blockchain_manager
        self.peers = []

    def connect_to_peer(self, peer_address):
        # Connect to a peer
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(peer_address)
        self.peers.append(sock)

    def broadcast_block(self, block):
        # Broadcast block to peers
        for peer in self.peers:
            peer.send(json.dumps(block).encode())

    def send_transaction(self, transaction):
        # Send transaction to peers
        for peer in self.peers:
            peer.send(json.dumps(transaction).encode())

    def receive_transaction(self, transaction):
        # Receive transaction from peers
        decrypted_transaction = self.blockchain_manager.transaction_manager.decrypt_transaction(transaction)
        return decrypted_transaction
