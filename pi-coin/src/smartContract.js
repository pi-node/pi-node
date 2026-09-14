// src/smartContract.js
const EventEmitter = require('events');

class SmartContract extends EventEmitter {
    constructor(contractData) {
        super();
        this.contractData = contractData; // Data defining the contract
        this.isActive = true; // Status of the contract
        this.executionHistory = []; // History of executions
    }

    // Execute the smart contract
    execute(executionData) {
        if (!this.isActive) {
            throw new Error("Contract is not active.");
        }

        // Validate execution conditions
        this.validateExecution(executionData);

        // Execute the contract logic
        this.executionHistory.push({
            executionData,
            timestamp: Date.now(),
        });

        // Emit an event for successful execution
        this.emit('executed', {
            contractData: this.contractData,
            executionData,
            timestamp: new Date().toISOString(),
        });

        console.log("Smart contract executed successfully:", this.contractData);
    }

    // Validate execution conditions
    validateExecution(executionData) {
        // Implement validation logic based on contract requirements
        // For example, check if the execution data meets certain criteria
        if (!executionData || typeof executionData !== 'object') {
            throw new Error("Invalid execution data.");
        }

        // Example: Check if a required field is present
        if (!executionData.requiredField) {
            throw new Error("Execution data must include 'requiredField'.");
        }
    }

    // Deactivate the smart contract
    deactivate() {
        this.isActive = false;
        console.log("Smart contract deactivated:", this.contractData);
    }

    // Reactivate the smart contract
    reactivate() {
        this.isActive = true;
        console.log("Smart contract reactivated:", this.contractData);
    }

    // Get execution history
    getExecutionHistory() {
        return this.executionHistory;
    }
}

// Example usage
const contract = new SmartContract({ terms: "Alice pays Bob 100 PI" });

// Listen for execution events
contract.on('executed', (event) => {
    console.log("Contract executed event:", event);
});

// Execute the contract
try {
    contract.execute({ requiredField: "Some data" });
    console.log("Execution history:", contract.getExecutionHistory());
} catch (error) {
    console.error(error.message);
}

// Deactivate the contract
contract.deactivate();

module.exports = SmartContract;
