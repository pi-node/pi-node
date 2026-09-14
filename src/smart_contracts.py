import json
import hashlib
from typing import Any, Dict, Callable, List, Optional

class SmartContract:
    def __init__(self, contract_name: str, owner: str):
        self.contract_name = contract_name
        self.owner = owner
        self.state: Dict[str, Any] = {}
        self.functions: Dict[str, Callable] = {}
        self.events: List[str] = []
        self.access_control: Dict[str, List[str]] = {}  # Role-based access control

    def add_function(self, func_name: str, func: Callable, roles: Optional[List[str]] = None):
        """Add a function to the smart contract with optional access control."""
        self.functions[func_name] = func
        if roles:
            self.access_control[func_name] = roles

    def call_function(self, func_name: str, caller: str, *args, **kwargs) -> Any:
        """Call a function in the smart contract with access control."""
        if func_name in self.functions:
            if self.has_access(caller, func_name):
                return self.functions[func_name](self, *args, **kwargs)
            else:
                raise Exception(f"Caller {caller} does not have access to function {func_name}")
        else:
            raise Exception(f"Function {func_name} not found in contract {self.contract_name}")

    def has_access(self, caller: str, func_name: str) -> bool:
        """Check if the caller has access to the function."""
        if func_name in self.access_control:
            return caller in self.access_control[func_name]
        return True  # Default to allow access if no restrictions

    def set_state(self, key: str, value: Any):
        """Set a value in the contract's state and emit an event."""
        self.state[key] = value
        self.emit_event(f"State updated: {key} = {value}")

    def get_state(self, key: str) -> Any:
        """Get a value from the contract's state."""
        return self.state.get(key, None)

    def emit_event(self, event: str):
        """Emit an event for state changes."""
        self.events.append(event)

    def get_events(self) -> List[str]:
        """Get the list of events that have occurred in the contract."""
        return self.events

    def to_dict(self) -> Dict[str, Any]:
        """Convert the smart contract to a dictionary for serialization."""
        return {
            "contract_name": self.contract_name,
            "owner": self.owner,
            "state": self.state,
            "events": self.events
        }

class SmartContractManager:
    def __init__(self):
        self.contracts: Dict[str, SmartContract] = {}

    def deploy_contract(self, contract_name: str, owner: str) -> SmartContract:
        """Deploy a new smart contract."""
        contract = SmartContract(contract_name, owner)
        self.contracts[contract_name] = contract
        return contract

    def get_contract(self, contract_name: str) -> SmartContract:
        """Retrieve a smart contract by name."""
        return self.contracts.get(contract_name)

    def save_contract_state(self, contract_name: str):
        """Persist the state of the contract to a file (or database)."""
        contract = self.get_contract(contract_name)
        if contract:
            with open(f"{contract_name}.json", "w") as f:
                json.dump(contract.to_dict(), f)

    def load_contract_state(self, contract_name: str):
        """Load the state of the contract from a file (or database)."""
        try:
            with open(f"{contract_name}.json", "r") as f:
                data = json.load(f)
                contract = SmartContract(data['contract_name'], data['owner'])
                contract.state = data['state']
                contract.events = data['events']
                self.contracts[contract_name] = contract
        except FileNotFoundError:
            raise Exception(f"Contract {contract_name} not found.")

# Example usage
if __name__ == "__main__":
    manager = SmartContractManager()

    # Deploy a new smart contract
    contract = manager.deploy_contract("MyContract", "Alice")

    # Add a function to the contract with access control
    def set_value(contract: SmartContract, key: str, value: Any):
        contract.set_state(key, value)

    contract.add_function("set_value", set_value, roles=["Alice"])

    # Call the function
    contract.call_function("set_value", "Alice", "my_key", "my_value")

    # Retrieve the state
    print("State:", contract.get_state("my_key"))
    print("Events:", contract.get_events())
    print("Contract Data:", json.dumps(contract.to_dict(), indent=4))

    # Save contract state
    manager.save_contract_state("MyContract")

    # Load contract state
    manager.load_contract_state("MyContract")
    print("Loaded State:", contract.get_state("my_key"))
