import unittest
import json
from src.smart_contracts import SmartContractManager, SmartContract

class TestSmartContract(unittest.TestCase):

    def setUp(self):
        """Set up a new smart contract manager for testing."""
        self.manager = SmartContractManager()
        self.contract = self.manager.deploy_contract("TestContract", "Alice")

    def test_add_function(self):
        """Test that a function can be added to the smart contract."""
        def dummy_function(contract: SmartContract):
            return "Hello, World!"

        self.contract.add_function("greet", dummy_function)
        self.assertIn("greet", self.contract.functions)

    def test_call_function(self):
        """Test that a function can be called successfully."""
        def return_value(contract: SmartContract):
            return "Test Value"

        self.contract.add_function("get_value", return_value)
        result = self.contract.call_function("get_value", "Alice")
        self.assertEqual(result, "Test Value")

    def test_access_control(self):
        """Test that access control works for functions."""
        def restricted_function(contract: SmartContract):
            return "Restricted Access"

        self.contract.add_function("restricted", restricted_function, roles=["Alice"])

        # Should succeed
        result = self.contract.call_function("restricted", "Alice")
        self.assertEqual(result, "Restricted Access")

        # Should raise an exception for unauthorized access
        with self.assertRaises(Exception) as context:
            self.contract.call_function("restricted", "Bob")
        self.assertEqual(str(context.exception), "Caller Bob does not have access to function restricted")

    def test_set_state(self):
        """Test that the state can be set and retrieved correctly."""
        self.contract.set_state("my_key", "my_value")
        self.assertEqual(self.contract.get_state("my_key"), "my_value")

    def test_event_logging(self):
        """Test that events are logged correctly."""
        self.contract.set_state("event_key", "event_value")
        events = self.contract.get_events()
        self.assertIn("State updated: event_key = event_value", events)

    def test_persist_and_load_contract_state(self):
        """Test that the contract state can be saved and loaded."""
        self.contract.set_state("persistent_key", "persistent_value")
        self.manager.save_contract_state("TestContract")

        # Create a new manager and load the contract state
        new_manager = SmartContractManager()
        new_manager.load_contract_state("TestContract")
        loaded_contract = new_manager.get_contract("TestContract")

        self.assertEqual(loaded_contract.get_state("persistent_key"), "persistent_value")

    def test_invalid_function_call(self):
        """Test that calling an invalid function raises an exception."""
        with self.assertRaises(Exception) as context:
            self.contract.call_function("non_existent_function", "Alice")
        self.assertEqual(str(context.exception), "Function non_existent_function not found in contract TestContract")

if __name__ == '__main__':
    unittest.main()
