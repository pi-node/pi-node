const crypto = require('crypto');

/**
 * Class representing a Transaction
 */
class Transaction {
    constructor(sender, receiver, amount) {
        this.sender = sender; // Sender's address
        this.receiver = receiver; // Receiver's address
        this.amount = amount; // Transaction amount
        this.timestamp = Date.now(); // Timestamp of the transaction
    }

    /**
     * Returns a string representation of the transaction
     */
    toString() {
        return JSON.stringify(this);
    }
}

/**
 * Class representing a Block in the blockchain
 */
class Block {
    constructor(index, previousHash, timestamp, transactions, hash, nonce) {
        this.index = index; // Block index
        this.previousHash = previousHash; // Hash of the previous block
        this.timestamp = timestamp; // Timestamp of block creation
        this.transactions = transactions; // Array of transactions
        this.hash = hash; // Hash of the current block
        this.nonce = nonce; // Nonce for proof of work
    }
}

/**
 * Class representing the Blockchain
 */
class Blockchain {
    constructor() {
        this.chain = []; // Array to hold the blockchain
        this.pendingTransactions = []; // Array to hold pending transactions
        this.createGenesisBlock(); // Create the first block
        this.difficulty = 2; // Difficulty for proof of work
    }

    /**
     * Creates the genesis block (the first block in the blockchain)
     */
    createGenesisBlock() {
        const genesisBlock = new Block(0, "0", Date.now(), [], this.calculateHash(0, "0", Date.now(), [], 0), 0);
        this.chain.push(genesisBlock);
    }

    /**
     * Calculates the hash of a block
     * @param {number} index - Block index
     * @param {string} previousHash - Hash of the previous block
     * @param {number} timestamp - Timestamp of block creation
     * @param {Array} transactions - Array of transactions
     * @param {number} nonce - Nonce for proof of work
     * @returns {string} - The calculated hash
     */
    calculateHash(index, previousHash, timestamp, transactions, nonce) {
        return crypto.createHash('sha256').update(index + previousHash + timestamp + JSON.stringify(transactions) + nonce).digest('hex');
    }

    /**
     * Adds a new transaction to the pending transactions
     * @param {Transaction} transaction - The transaction to add
     */
    addTransaction(transaction) {
        if (!transaction.sender || !transaction.receiver || !transaction.amount) {
            throw new Error("Invalid transaction");
        }
        this.pendingTransactions.push(transaction);
    }

    /**
     * Creates a new block and adds it to the blockchain
     * @returns {Block} - The newly created block
     */
    mineBlock() {
        const previousBlock = this.chain[this.chain.length - 1];
        const newIndex = previousBlock.index + 1;
        const newTimestamp = Date.now();
        let nonce = 0;
        let hash;

        // Proof of Work
        do {
            nonce++;
            hash = this.calculateHash(newIndex, previousBlock.hash, newTimestamp, this.pendingTransactions, nonce);
        } while (hash.substring(0, this.difficulty) !== Array(this.difficulty + 1).join("0"));

        const newBlock = new Block(newIndex, previousBlock.hash, newTimestamp, this.pendingTransactions, hash, nonce);
        this.chain.push(newBlock);
        this.pendingTransactions = []; // Reset pending transactions
        return newBlock;
    }

    /**
     * Gets the entire blockchain
     * @returns {Array} - The blockchain
     */
    getChain() {
        return this.chain;
    }
}

/**
 * Example usage of the Blockchain class
 */
function main() {
    const piCoinBlockchain = new Blockchain();

    // Adding transactions
    piCoinBlockchain.addTransaction(new Transaction("Alice", "Bob", 10));
    piCoinBlockchain.addTransaction(new Transaction("Bob", "Charlie", 20));
    piCoinBlockchain.addTransaction(new Transaction("Charlie", "Alice", 15));

    // Mining a block
    const minedBlock = piCoinBlockchain.mineBlock();
    console.log("Mined Block:");
    console.log(JSON.stringify(minedBlock, null, 2));

    // Display the blockchain
    console.log("Pi Coin Blockchain:");
    console.log(JSON.stringify(piCoinBlockchain.getChain(), null, 2));
}

// Run the example
main();

module.exports = Blockchain;
