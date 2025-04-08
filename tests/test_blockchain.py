import unittest
import hashlib
import json
import rsa
from blockchain import Blockchain  # Assuming your blockchain code is in a file named blockchain.py

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        """Set up a new blockchain instance for testing."""
        self.blockchain = Blockchain()
        self.username = "test_user"
        self.password = "test_password"
        self.blockchain.register_user(self.username, self.password)

    def test_user_registration(self):
        """Test user registration."""
        self.assertIn(self.username, self.blockchain.users)
        self.assertEqual(self.blockchain.users[self.username], hashlib.sha256(self.password.encode()).hexdigest())

    def test_user_authentication(self):
        """Test user authentication with correct credentials."""
        self.assertTrue(self.blockchain.authenticate_user(self.username, self.password))

    def test_user_authentication_failure(self):
        """Test user authentication with incorrect credentials."""
        self.assertFalse(self.blockchain.authenticate_user(self.username, "wrong_password"))

    def test_transaction_signing_and_verification(self):
        """Test transaction signing and verification."""
        private_key, public_key = rsa.newkeys(512)
        transaction = {"sender": "Alice", "recipient": "Bob", "amount": 50.0}
        signature = self.blockchain.sign_transaction(private_key, transaction)

        self.assertTrue(self.blockchain.verify_signature(public_key, signature, transaction))

    def test_invalid_signature(self):
        """Test verification of an invalid signature."""
        private_key, public_key = rsa.newkeys(512)
        transaction = {"sender": "Alice", "recipient": "Bob", "amount": 50.0}
        signature = self.blockchain.sign_transaction(private_key, transaction)

        # Modify the transaction to create an invalid signature
        transaction["amount"] = 100.0
        self.assertFalse(self.blockchain.verify_signature(public_key, signature, transaction))

    def test_add_transaction(self):
        """Test adding a valid transaction."""
        private_key, public_key = rsa.newkeys(512)
        transaction = {"sender": "Alice", "recipient": "Bob", "amount": 50.0}
        signature = self.blockchain.sign_transaction(private_key, transaction)

        self.blockchain.add_transaction(transaction["sender"], transaction["recipient"], transaction["amount"], signature)
        self.assertEqual(len(self.blockchain.current_transactions), 1)

    def test_mine_block(self):
        """Test mining a new block."""
        private_key, public_key = rsa.newkeys(512)
        transaction = {"sender": "Alice", "recipient": "Bob", "amount": 50.0}
        signature = self.blockchain.sign_transaction(private_key, transaction)

        self.blockchain.add_transaction(transaction["sender"], transaction["recipient"], transaction["amount"], signature)
        new_block = self.blockchain.mine_block()

        self.assertEqual(new_block.index, 1)
        self.assertEqual(len(new_block.transactions), 1)

    def test_validate_chain(self):
        """Test chain validation."""
        self.assertTrue(self.blockchain.validate_chain())

        # Tamper with the blockchain
        self.blockchain.chain[1].transactions[0]["amount"] = 100.0
        self.assertFalse(self.blockchain.validate_chain())

    def test_get_chain(self):
        """Test getting the blockchain."""
        chain = self.blockchain.get_chain()
        self.assertEqual(len(chain), 1)  # Only the genesis block should be present initially

        # Mine a block
        private_key, public_key = rsa.newkeys(512)
        transaction = {"sender": "Alice", "recipient": "Bob", "amount": 50.0}
        signature = self.blockchain.sign_transaction(private_key, transaction)
        self.blockchain.add_transaction(transaction["sender"], transaction["recipient"], transaction["amount"], signature)
        self.blockchain.mine_block()

        chain = self.blockchain.get_chain()
        self.assertEqual(len(chain), 2)  # Now there should be the genesis block and one mined block

if __name__ == "__main__":
    unittest.main()
