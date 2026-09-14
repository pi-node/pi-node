// src/blockchain.js
const crypto = require('crypto');
const PI_COIN = require('./constant');

class Block {
    constructor(index, previousHash, timestamp, transactions, hash, nonce) {
        this.index = index;
        this.previousHash = previousHash;
        this.timestamp = timestamp;
        this.transactions = transactions; // Array of transactions
        this.hash = hash;
        this.nonce = nonce; // Nonce for proof of work
    }
}

class Blockchain {
    constructor() {
        this.chain = [this.createGenesisBlock()];
        this.pendingTransactions = []; // Transactions to be added to the next block
        this.difficulty = 4; // Difficulty for mining
        this.miningReward = 100; // Reward for mining a block
    }

    createGenesisBlock() {
        return new Block(0, "0", Date.now(), [], this.calculateHash(0, "0", Date.now(), [], 0), 0);
    }

    calculateHash(index, previousHash, timestamp, transactions, nonce) {
        return crypto.createHash('sha256').update(index + previousHash + timestamp + JSON.stringify(transactions) + nonce).digest('hex');
    }

    mineBlock(minerAddress) {
        const previousBlock = this.chain[this.chain.length - 1];
        const index = previousBlock.index + 1;
        const timestamp = Date.now();
        const nonce = this.proofOfWork(previousBlock.hash);
        const block = new Block(index, previousBlock.hash, timestamp, this.pendingTransactions, this.calculateHash(index, previousBlock.hash, timestamp, this.pendingTransactions, nonce), nonce);
        
        this.chain.push(block);
        this.pendingTransactions = []; // Reset pending transactions
        this.addTransaction(new Transaction(null, minerAddress, this.miningReward)); // Reward the miner
        console.log(`Block mined: ${block.hash}`);
    }

    proofOfWork(previousHash) {
        let nonce = 0;
        let hash;
        do {
            nonce++;
            hash = this.calculateHash(this.chain.length, previousHash, Date.now(), this.pendingTransactions, nonce);
        } while (hash.substring(0, this.difficulty) !== Array(this.difficulty + 1).join("0")); // Check for leading zeros
        return nonce;
    }

    addTransaction(transaction) {
        if (!transaction.sender || !transaction.receiver || !transaction.amount) {
            throw new Error("Invalid transaction.");
        }
        this.pendingTransactions.push(transaction);
    }

    validateChain() {
        for (let i = 1; i < this.chain.length; i++) {
            const currentBlock = this.chain[i];
            const previousBlock = this.chain[i - 1];

            // Check if the hash is correct
            if (currentBlock.hash !== this.calculateHash(currentBlock.index, currentBlock.previousHash, currentBlock.timestamp, currentBlock.transactions, currentBlock.nonce)) {
                return false;
            }

            // Check if the previous block's hash is correct
            if (currentBlock.previousHash !== previousBlock.hash) {
                return false;
            }
        }
        return true;
    }
}

module.exports = Blockchain;
