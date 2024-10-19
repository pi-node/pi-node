import unittest
import logging

# Configure logging
logging.basicConfig(filename='unit_tests.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sample functions to be tested
def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b

def multiply(a, b):
    """Return the product of two numbers."""
    return a * b

def divide(a, b):
    """Return the quotient of two numbers. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

class TestMathOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up any state specific to the test class."""
        logging.info("Setting up unit tests.")

    @classmethod
    def tearDownClass(cls):
        """Clean up any state specific to the test class."""
        logging.info("Tearing down unit tests.")

    def test_add(self):
        """Test the add function."""
        logging.info("Testing add function.")
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        """Test the subtract function."""
        logging.info("Testing subtract function.")
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 0), 0)
        self.assertEqual(subtract(-1, -1), 0)

    def test_multiply(self):
        """Test the multiply function."""
        logging.info("Testing multiply function.")
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 1), -1)
        self.assertEqual(multiply(0, 5), 0)

    def test_divide(self):
        """Test the divide function."""
        logging.info("Testing divide function.")
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(-6, -3), 2)
        with self.assertRaises(ValueError):
            divide(1, 0)

if __name__ == "__main__":
    logging.info("Starting unit tests.")
    unittest.main()
