const EventEmitter = require('events');
const Transaction = require('../blockchain/transaction');
const Ledger = require('../blockchain/ledger');

/**
 * Class representing a Real-Time Monitor
 */
class RealTimeMonitor extends EventEmitter {
    constructor() {
        super();
        this.ledger = new Ledger();
        this.setupListeners();
    }

    /**
     * Sets up event listeners for monitoring transactions
     */
    setupListeners() {
        this.on('transactionAdded', (transaction) => {
            console.log(`New transaction added: ${transaction.toString()}`);
            console.log(`Current balance of ${transaction.sender}: ${this.ledger.getBalance(transaction.sender)}`);
            console.log(`Current balance of ${transaction.receiver}: ${this.ledger.getBalance(transaction.receiver)}`);
        });
    }

    /**
     * Adds a transaction to the ledger and emits an event
     * @param {Transaction} transaction - The transaction to add
     */
    addTransaction(transaction) {
        this.ledger.addTransaction(transaction);
        this.emit('transactionAdded', transaction);
    }

    /**
     * Displays the current state of the ledger
     */
    displayLedger() {
        this.ledger.displayLedger();
    }
}

/**
 * Example usage of the Real-Time Monitor
 */
function main() {
    const monitor = new RealTimeMonitor();

    // Create and add valid transactions
    const transaction1 = new Transaction("Alice", "Bob", 50);
    monitor.addTransaction(transaction1);

    const transaction2 = new Transaction("Bob", "Charlie", 30);
    monitor.addTransaction(transaction2);

    const transaction3 = new Transaction("Alice", "Charlie", 20);
    monitor.addTransaction(transaction3);

    // Display the current state of the ledger
    monitor.displayLedger();
}

// Run the example
main();

module.exports = RealTimeMonitor;
