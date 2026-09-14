const fs = require('fs');
const path = require('path');

/**
 * Class representing a Logging System
 */
class Logger {
    constructor(logFilePath) {
        this.logFilePath = logFilePath; // Path to the log file
        this.ensureLogFileExists(); // Ensure the log file exists
    }

    /**
     * Ensures the log file exists
     */
    ensureLogFileExists() {
        const dir = path.dirname(this.logFilePath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true }); // Create directory if it doesn't exist
        }
        if (!fs.existsSync(this.logFilePath)) {
            fs.writeFileSync(this.logFilePath, ''); // Create the log file if it doesn't exist
        }
    }

    /**
     * Logs a message to the log file
     * @param {string} message - The message to log
     */
    log(message) {
        const timestamp = new Date().toISOString(); // Get the current timestamp
        const logEntry = `${timestamp} - ${message}\n`; // Format the log entry
        fs.appendFileSync(this.logFilePath, logEntry); // Append the log entry to the file
    }

    /**
     * Logs a transaction
     * @param {Transaction} transaction - The transaction to log
     */
    logTransaction(transaction) {
        const logMessage = `Transaction: ${transaction.toString()}`;
        this.log(logMessage); // Log the transaction
    }

    /**
     * Logs an event
     * @param {string} event - The event to log
     */
    logEvent(event) {
        const logMessage = `Event: ${event}`;
        this.log(logMessage); // Log the event
    }
}

/**
 * Example usage of the Logger class
 */
function main() {
    const logger = new Logger('./src/logs/transactions.log'); // Specify the log file path

    // Simulate logging transactions
    const transaction1 = { sender: "Alice", receiver: "Bob", amount: 50, toString: () => "Alice -> Bob: $50" };
    const transaction2 = { sender: "Bob", receiver: "Charlie", amount: 30, toString: () => "Bob -> Charlie: $30" };

    logger.logTransaction(transaction1);
    logger.logTransaction(transaction2);

    // Simulate logging events
    logger.logEvent("New block mined.");
    logger.logEvent("Transaction added to the ledger.");
}

// Run the example
main();

module.exports = Logger;
