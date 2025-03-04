const EventEmitter = require('events');

/**
 * Class representing an Alert System
 */
class AlertSystem extends EventEmitter {
    constructor(thresholdAmount) {
        super();
        this.thresholdAmount = thresholdAmount; // Threshold for large transactions
        this.suspiciousAccounts = new Set(); // Set to hold suspicious accounts
        this.setupListeners();
    }

    /**
     * Sets up event listeners for monitoring transactions
     */
    setupListeners() {
        this.on('transactionAdded', (transaction) => {
            this.checkForSuspiciousActivity(transaction);
        });
    }

    /**
     * Checks for suspicious activity based on transaction details
     * @param {Transaction} transaction - The transaction to check
     */
    checkForSuspiciousActivity(transaction) {
        // Check for large transactions
        if (transaction.amount > this.thresholdAmount) {
            console.log(`ALERT: Large transaction detected! ${transaction.toString()}`);
        }

        // Check for transactions from suspicious accounts
        if (this.suspiciousAccounts.has(transaction.sender)) {
            console.log(`ALERT: Transaction from suspicious account detected! ${transaction.toString()}`);
        }
    }

    /**
     * Adds an account to the list of suspicious accounts
     * @param {string} account - The account to mark as suspicious
     */
    addSuspiciousAccount(account) {
        this.suspiciousAccounts.add(account);
        console.log(`Account ${account} has been marked as suspicious.`);
    }

    /**
     * Removes an account from the list of suspicious accounts
     * @param {string} account - The account to remove from suspicious list
     */
    removeSuspiciousAccount(account) {
        this.suspiciousAccounts.delete(account);
        console.log(`Account ${account} has been removed from the suspicious list.`);
    }
}

/**
 * Example usage of the Alert System
 */
function main() {
    const alertSystem = new AlertSystem(100); // Set threshold for large transactions

    // Add a suspicious account
    alertSystem.addSuspiciousAccount("Eve");

    // Simulate adding transactions
    const transaction1 = { sender: "Alice", receiver: "Bob", amount: 50, toString: () => "Alice -> Bob: $50" };
    const transaction2 = { sender: "Eve", receiver: "Charlie", amount: 200, toString: () => "Eve -> Charlie: $200" };
    const transaction3 = { sender: "Bob", receiver: "Eve", amount: 30, toString: () => "Bob -> Eve: $30" };

    // Emit transaction added events
    alertSystem.emit('transactionAdded', transaction1);
    alertSystem.emit('transactionAdded', transaction2);
    alertSystem.emit('transactionAdded', transaction3);
}

// Run the example
main();

module.exports = AlertSystem;
