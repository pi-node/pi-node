import unittest
from src.blockchain import Blockchain, Block

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        """Set up a new blockchain for testing."""
        self.blockchain = Blockchain()

    def test_genesis_block(self):
        """Test that the genesis block is created correctly."""
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block.index, 0)
        self.assertEqual(genesis_block.previous_hash, "0")
        self.assertEqual(genesis_block.data, "Genesis Block")
        self.assertIsNotNone(genesis_block.timestamp)
        self.assertIsNotNone(genesis_block.hash)

    def test_add_block(self):
        """Test adding a new block to the blockchain."""
        previous_length = len(self.blockchain.chain)
        new_block = self.blockchain.add_block("Test Block Data")
        
        self.assertEqual(len(self.blockchain.chain), previous_length + 1)
        self.assertEqual(new_block.data, "Test Block Data")
        self.assertEqual(new_block.index, previous_length)
        self.assertEqual(new_block.previous_hash, self.blockchain.chain[-2].hash)

    def test_block_hash(self):
        """Test that the hash of a block is correct."""
        block_data = "Test Block Data"
        block = Block(1, self.blockchain.chain[0].hash, 1234567890, block_data, "")
        block.hash = self.blockchain.hash_block(block.index, block.previous_hash, block.timestamp, block.data)
        
        self.assertEqual(block.hash, self.blockchain.hash_block(block.index, block.previous_hash, block.timestamp, block.data))

    def test_validate_chain(self):
        """Test that the blockchain validates correctly."""
        self.assertTrue(self.blockchain.validate_chain())
        self.blockchain.add_block("Test Block Data")
        self.assertTrue(self.blockchain.validate_chain())

        # Tamper with the blockchain
        self.blockchain.chain[1].data = "Tampered Data"
        self.assertFalse(self.blockchain.validate_chain())

    def test_get_chain(self):
        """Test that the get_chain method returns the correct data."""
        self.blockchain.add_block("First Block")
        self.blockchain.add_block("Second Block")
        
        chain_data = self.blockchain.get_chain()
        self.assertEqual(len(chain_data), 3)  # 2 added blocks + genesis block
        self.assertEqual(chain_data[0]['data'], "Genesis Block")
        self.assertEqual(chain_data[1]['data'], "First Block")
        self.assertEqual(chain_data[2]['data'], "Second Block")

if __name__ == '__main__':
    unittest.main()
