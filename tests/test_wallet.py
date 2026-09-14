import unittest
import os
from src.wallet import Wallet

class TestWallet(unittest.TestCase):

    def setUp(self):
        """Set up a new wallet for testing."""
        self.password = "test_password"
        self.wallet = Wallet(self.password)

    def test_generate_address(self):
        """Test that a new address can be generated."""
        initial_address_count = len(self.wallet.addresses)
        new_address = self.wallet.generate_address(initial_address_count)
        self.assertNotIn(new_address, self.wallet.addresses)
        self.wallet.addresses[new_address] = 0.0  # Add the new address to the wallet
        self.assertEqual(len(self.wallet.addresses), initial_address_count + 1)

    def test_get_balance(self):
        """Test that the balance of an address can be retrieved."""
        address = self.wallet.generate_address(0)
        self.assertEqual(self.wallet.get_balance(address), 0.0)

        # Set a balance and check
        self.wallet.addresses[address] = 50.0
        self.assertEqual(self.wallet.get_balance(address), 50.0)

    def test_create_transaction(self):
        """Test that a transaction can be created successfully."""
        address1 = self.wallet.generate_address(0)
        address2 = self.wallet.generate_address(1)

        # Set initial balances
        self.wallet.addresses[address1] = 100.0
        self.wallet.addresses[address2] = 0.0

        # Create a transaction
        success = self.wallet.create_transaction(address1, address2, 50.0)
        self.assertTrue(success)
        self.assertEqual(self.wallet.get_balance(address1), 50.0)
        self.assertEqual(self.wallet.get_balance(address2), 50.0)

    def test_create_transaction_insufficient_balance(self):
        """Test that a transaction fails with insufficient balance."""
        address1 = self.wallet.generate_address(0)
        address2 = self.wallet.generate_address(1)

        # Set initial balances
        self.wallet.addresses[address1] = 10.0
        self.wallet.addresses[address2] = 0.0

        with self.assertRaises(Exception) as context:
            self.wallet.create_transaction(address1, address2, 50.0)
        self.assertEqual(str(context.exception), "Insufficient balance.")

    def test_create_transaction_nonexistent_address(self):
        """Test that a transaction fails with a nonexistent address."""
        address1 = self.wallet.generate_address(0)
        address2 = "nonexistent_address"

        # Set initial balance
        self.wallet.addresses[address1] = 100.0

        with self.assertRaises(Exception) as context:
            self.wallet.create_transaction(address1, address2, 50.0)
        self.assertEqual(str(context.exception), "To address does not exist.")

    def test_save_and_load_wallet(self):
        """Test that the wallet can be saved and loaded correctly."""
        address1 = self.wallet.generate_address(0)
        self.wallet.addresses[address1] = 100.0
        self.wallet.save_wallet("test_wallet.json")

        # Create a new wallet and load the saved wallet
        new_wallet = Wallet(self.password)
        new_wallet.load_wallet("test_wallet.json")

        self.assertEqual(new_wallet.get_balance(address1), 100.0)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists("test_wallet.json"):
            os.remove("test_wallet.json")

if __name__ == '__main__':
    unittest.main()
