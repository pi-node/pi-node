import hashlib
import time
import json
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, data: Any, hash: str):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def to_dict(self) -> Dict[str, Any]:
        """Convert the block to a dictionary for easy serialization."""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.hash_block(0, "0", time.time(), "Genesis Block"))
        self.chain.append(genesis_block)

    def hash_block(self, index: int, previous_hash: str, timestamp: float, data: Any) -> str:
        """Create a SHA-256 hash of a block."""
        block_string = json.dumps({
            "index": index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "data": data
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, data: Any) -> Block:
        """Add a new block to the blockchain."""
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = time.time()
        hash_value = self.hash_block(index, previous_block.hash, timestamp, data)
        new_block = Block(index, previous_block.hash, timestamp, data, hash_value)
        self.chain.append(new_block)
        return new_block

    def validate_chain(self) -> bool:
        """Validate the entire blockchain to ensure integrity."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash of the current block is correct
            if current_block.hash != self.hash_block(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                return False

            # Check if the previous hash of the current block matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
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
