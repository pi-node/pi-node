import unittest
from src.transaction import Transaction, TransactionPool

class TestTransaction(unittest.TestCase):

    def setUp(self):
        """Set up a new transaction for testing."""
        self.transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)

    def test_transaction_creation(self):
        """Test that a transaction is created correctly."""
        self.assertEqual(self.transaction.sender, "Alice")
        self.assertEqual(self.transaction.recipient, "Bob")
        self.assertEqual(self.transaction.amount, 10.0)
        self.assertIsNotNone(self.transaction.transaction_id)

    def test_transaction_id(self):
        """Test that the transaction ID is unique and correctly generated."""
        transaction_1 = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        transaction_2 = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        self.assertNotEqual(transaction_1.transaction_id, transaction_2.transaction_id)

    def test_transaction_to_dict(self):
        """Test that the transaction can be converted to a dictionary."""
        transaction_dict = self.transaction.to_dict()
        self.assertEqual(transaction_dict['sender'], "Alice")
        self.assertEqual(transaction_dict['recipient'], "Bob")
        self.assertEqual(transaction_dict['amount'], 10.0)
        self.assertEqual(transaction_dict['transaction_id'], self.transaction.transaction_id)

class TestTransactionPool(unittest.TestCase):

    def setUp(self):
        """Set up a new transaction pool for testing."""
        self.transaction_pool = TransactionPool()

    def test_add_transaction(self):
        """Test adding a valid transaction to the pool."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        self.transaction_pool.add_transaction(transaction)
        self.assertEqual(len(self.transaction_pool.transactions), 1)

    def test_validate_transaction(self):
        """Test that a transaction is validated correctly."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        self.assertTrue(self.transaction_pool.validate_transaction(transaction))

    def test_get_transactions(self):
        """Test that the transaction pool returns the correct transactions."""
        transaction_1 = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        transaction_2 = Transaction(sender="Charlie", recipient="Dave", amount=20.0)
        self.transaction_pool.add_transaction(transaction_1)
        self.transaction_pool.add_transaction(transaction_2)

        transactions = self.transaction_pool.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['sender'], "Alice")
        self.assertEqual(transactions[1]['sender'], "Charlie")

    def test_clear_transactions(self):
        """Test that the transaction pool can be cleared."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        self.transaction_pool.add_transaction(transaction)
        self.transaction_pool.clear_transactions()
        self.assertEqual(len(self.transaction_pool.transactions), 0)

if __name__ == '__main__':
    unittest.main()
