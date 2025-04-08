import hashlib
import time
import json
from typing import List, Dict, Any, Optional
import random
import string

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, transactions: List[Dict[str, Any]], hash: str, nonce: int):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.hash = hash
        self.nonce = nonce

    def to_dict(self) -> Dict[str, Any]:
        """Convert the block to a dictionary for easy serialization."""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "hash": self.hash,
            "nonce": self.nonce
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.current_transactions: List[Dict[str, Any]] = []
        self.pi_value = 314159.00  # Set the value of Pi Coin
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(0, "0", time.time(), [], self.hash_block(0, "0", time.time(), [], 0), 0)
        self.chain.append(genesis_block)

    def hash_block(self, index: int, previous_hash: str, timestamp: float, transactions: List[Dict[str, Any]], nonce: int) -> str:
        """Create a SHA-256 hash of a block."""
        block_string = json.dumps({
            "index": index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "transactions": transactions,
            "nonce": nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_transaction(self, sender: str, recipient: str, amount: float) -> None:
        """Add a new transaction to the list of transactions."""
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": time.time()
        })

    def mine_block(self) -> Block:
        """Mine a new block and add it to the blockchain."""
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = time.time()
        nonce = self.proof_of_work(previous_block.nonce)
        hash_value = self.hash_block(index, previous_block.hash, timestamp, self.current_transactions, nonce)

        new_block = Block(index, previous_block.hash, timestamp, self.current_transactions, hash_value, nonce)
        self.chain.append(new_block)
        self.current_transactions = []  # Reset the current transactions
        return new_block

    def proof_of_work(self, last_nonce: int) -> int:
        """Simple Proof of Work algorithm."""
        nonce = 0
        while not self.valid_proof(last_nonce, nonce):
            nonce += 1
        return nonce

    def valid_proof(self, last_nonce: int, nonce: int) -> bool:
        """Validates the proof of work."""
        guess = f'{last_nonce}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Difficulty level

    def validate_chain(self) -> bool:
        """Validate the entire blockchain to ensure integrity."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash of the current block is correct
            if current_block.hash != self.hash_block(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.transactions, current_block.nonce):
                return False

            # Check if the previous hash of the current block matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_chain(self) -> List[Dict[str, Any]]:
        """Get the blockchain as a list of dictionaries."""
        return [block.to_dict() for block in self.chain]

    def get_pi_value (self) -> float:
        """Get the current value of Pi Coin."""
        return self.pi_value

    def set_pi_value(self, new_value: float) -> None:
        """Set a new value for Pi Coin."""
        self.pi_value = new_value

    def authenticate_user(self, username: str, password: str) -> bool:
        """Simple user authentication (placeholder)."""
        # In a real application, this would check against a database
        return username == "admin" and password == "password"

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Simulate user authentication
    if blockchain.authenticate_user("admin", "password"):
        blockchain.add_transaction("Alice", "Bob", 50.0)
        blockchain.add_transaction("Bob", "Charlie", 25.0)
        
        # Mine a new block
        blockchain.mine_block()

        print("Blockchain valid:", blockchain.validate_chain())
        print("Blockchain:", blockchain.get_chain())
        print("Current Pi Coin Value: $", blockchain.get_pi_value())
    else:
        print("Authentication failed.")
