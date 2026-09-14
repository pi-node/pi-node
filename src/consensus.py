import hashlib
import time
import json
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, data: Any, hash: str, nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

    def to_dict(self) -> Dict[str, Any]:
        """Convert the block to a dictionary for easy serialization."""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash,
            "nonce": self.nonce
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty: int = 4  # Initial difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.hash_block(0, "0", time.time(), "Genesis Block", 0))
        self.chain.append(genesis_block)

    def hash_block(self, index: int, previous_hash: str, timestamp: float, data: Any, nonce: int) -> str:
        """Create a SHA-256 hash of a block."""
        block_string = json.dumps({
            "index": index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "data": data,
            "nonce": nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, data: Any) -> Block:
        """Add a new block to the blockchain using Proof of Work."""
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = time.time()
        nonce, hash_value = self.proof_of_work(index, previous_block.hash, timestamp, data)
        new_block = Block(index, previous_block.hash, timestamp, data, hash_value, nonce)
        self.chain.append(new_block)
        self.adjust_difficulty()
        return new_block

    def proof_of_work(self, index: int, previous_hash: str, timestamp: float, data: Any) -> (int, str):
        """Perform Proof of Work to find a valid nonce."""
        nonce = 0
        while True:
            hash_value = self.hash_block(index, previous_hash, timestamp, data, nonce)
            if hash_value[:self.difficulty] == "0" * self.difficulty:  # Check if hash meets difficulty
                logging.info(f"Block mined: {index} with nonce: {nonce}")
                return nonce, hash_value
            nonce += 1

    def adjust_difficulty(self):
        """Adjust the mining difficulty based on the time taken to mine recent blocks."""
        if len(self.chain) < 2:
            return  # Not enough blocks to adjust difficulty

        # Calculate the time taken to mine the last block
        last_block = self.chain[-1]
        second_last_block = self.chain[-2]
        time_taken = last_block.timestamp - second_last_block.timestamp

        # Adjust difficulty based on time taken
        if time_taken < 2:  # If it took less than 2 seconds, increase difficulty
            self.difficulty += 1
            logging.info(f"Increasing difficulty to: {self.difficulty}")
        elif time_taken > 10:  # If it took more than 10 seconds, decrease difficulty
            self.difficulty = max(1, self.difficulty - 1)  # Ensure difficulty doesn't go below 1
            logging.info(f"Decreasing difficulty to: {self.difficulty}")

    def validate_chain(self) -> bool:
        """Validate the entire blockchain to ensure integrity."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash of the current block is correct
            if current_block.hash != self.hash_block(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data, current_block.nonce):
                logging.error("Invalid hash for block index: {}".format(current_block.index))
                return False

            # Check if the previous hash of the current block matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                logging.error("Invalid previous hash for block index: {}".format(current_block.index))
                return False

        return True

    def get_chain(self) -> List[Dict[str, Any]]:
        """Get the blockchain as a list of dictionaries."""
        return [block.to_dict() for block in self.chain]

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_block("First block data")
    blockchain.add_block("Second block data")

    print("Blockchain valid:", blockchain.validate_chain())
    print("Blockchain:", blockchain.get_chain())
