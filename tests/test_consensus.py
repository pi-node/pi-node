import unittest
import time
from src.consensus import Blockchain, Block

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        """Set up a new blockchain for testing."""
        self.blockchain = Blockchain()

    def test_create_genesis_block(self):
        """Test that the genesis block is created correctly."""
        self.assertEqual(len(self.blockchain.chain), 1)
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block.index, 0)
        self.assertEqual(genesis_block.previous_hash, "0")
        self.assertEqual(genesis_block.data, "Genesis Block")

    def test_add_block(self):
        """Test that a new block can be added to the blockchain."""
        self.blockchain.add_block("First block data")
        self.assertEqual(len(self.blockchain.chain), 2)
        new_block = self.blockchain.chain[1]
        self.assertEqual(new_block.data, "First block data")
        self.assertEqual(new_block.index, 1)
        self.assertEqual(new_block.previous_hash, self.blockchain.chain[0].hash)

    def test_proof_of_work(self):
        """Test that the proof of work generates a valid block."""
        previous_block = self.blockchain.chain[-1]
        index = previous_block.index + 1
        timestamp = time.time()
        data = "Test block data"
        nonce, hash_value = self.blockchain.proof_of_work(index, previous_block.hash, timestamp, data)
        
        # Check if the hash meets the difficulty requirement
        self.assertTrue(hash_value.startswith("0" * self.blockchain.difficulty))

    def test_validate_chain(self):
        """Test that the blockchain validates correctly."""
        self.assertTrue(self.blockchain.validate_chain())
        self.blockchain.add_block("First block data")
        self.assertTrue(self.blockchain.validate_chain())

        # Tamper with the blockchain
        self.blockchain.chain[1].data = "Tampered data"
        self.assertFalse(self.blockchain.validate_chain())

    def test_adjust_difficulty(self):
        """Test that the difficulty adjusts correctly based on mining time."""
        initial_difficulty = self.blockchain.difficulty
        self.blockchain.add_block("First block data")
        self.blockchain.add_block("Second block data")
        
        # Simulate fast mining
        self.blockchain.difficulty = initial_difficulty + 1
        self.blockchain.add_block("Third block data")
        self.assertGreater(self.blockchain.difficulty, initial_difficulty)

        # Simulate slow mining
        self.blockchain.difficulty = initial_difficulty - 1
        self.blockchain.add_block("Fourth block data")
        self.assertLess(self.blockchain.difficulty, initial_difficulty)

    def test_get_chain(self):
        """Test that the blockchain can be retrieved as a list of dictionaries."""
        self.blockchain.add_block("First block data")
        chain_data = self.blockchain.get_chain()
        self.assertEqual(len(chain_data), 2)
        self.assertEqual(chain_data[0]['data'], "Genesis Block")
        self.assertEqual(chain_data[1]['data'], "First block data")

if __name__ == '__main__':
    unittest.main()
