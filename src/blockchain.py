import hashlib
import time
import json
from typing import List, Dict, Any
import random
import string
import rsa  # For digital signatures

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
        self.users = {}  # Store user credentials

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

    def add_transaction(self, sender: str, recipient: str, amount: float, signature: str) -> None:
        """Add a new transaction to the list of transactions."""
        if self.verify_signature(sender, signature):
            self.current_transactions.append({
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
                "timestamp": time.time()
            })
        else:
            raise ValueError("Invalid transaction signature.")

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

    def get_chain(self) -> List[Dict [str, Any]]:
        """Get the blockchain as a list of dictionaries."""
        return [block.to_dict() for block in self.chain]

    def get_pi_value(self) -> float:
        """Get the current value of Pi Coin."""
        return self.pi_value

    def set_pi_value(self, new_value: float) -> None:
        """Set a new value for Pi Coin."""
        self.pi_value = new_value

    def register_user(self, username: str, password: str) -> None:
        """Register a new user with a hashed password."""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = hashed_password

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user using hashed password."""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return self.users.get(username) == hashed_password

    def sign_transaction(self, private_key, transaction: Dict[str, Any]) -> str:
        """Sign a transaction using the user's private key."""
        transaction_string = json.dumps(transaction, sort_keys=True).encode()
        return rsa.sign(transaction_string, private_key, 'SHA-256')

    def verify_signature(self, public_key, signature: str, transaction: Dict[str, Any]) -> bool:
        """Verify the transaction signature."""
        transaction_string = json.dumps(transaction, sort_keys=True).encode()
        try:
            rsa.verify(transaction_string, signature, public_key)
            return True
        except rsa.VerificationError:
            return False

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Register a user
    blockchain.register_user("admin", "password")
    
    # Simulate user authentication
    if blockchain.authenticate_user("admin", "password"):
        # Create a transaction
        sender = "Alice"
        recipient = "Bob"
        amount = 50.0
        private_key, public_key = rsa.newkeys(512)  # Generate RSA keys
        transaction = {"sender": sender, "recipient": recipient, "amount": amount}
        signature = blockchain.sign_transaction(private_key, transaction)
        
        # Add the transaction to the blockchain
        blockchain.add_transaction(sender, recipient, amount, signature)
        
        # Mine a new block
        blockchain.mine_block()

        print("Blockchain valid:", blockchain.validate_chain())
        print("Blockchain:", blockchain.get_chain())
        print("Current Pi Coin Value: $", blockchain.get_pi_value())
    else:
        print("Authentication failed.")
