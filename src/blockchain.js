// src/blockchain.js
const crypto = require('crypto');
const PI_COIN = require('./constant');

class Block {
    constructor(index, previousHash, timestamp, data, hash) {
        this.index = index;
        this.previousHash = previousHash;
        this.timestamp = timestamp;
        this.data = data;
        this.hash = hash;
    }
}

class Blockchain {
    constructor() {
        this.chain = [this.createGenesisBlock()];
    }

    createGenesisBlock() {
        return new Block(0, "0", Date.now(), "Genesis Block", this.calculateHash(0, "0", Date.now(), "Genesis Block"));
    }

    calculateHash(index, previousHash, timestamp, data) {
        return crypto.createHash('sha256').update(index + previousHash + timestamp + JSON.stringify(data)).digest('hex');
    }

    addBlock(data) {
        const previousBlock = this.chain[this.chain.length - 1];
        const newIndex = previousBlock.index + 1;
        const newTimestamp = Date.now();
        const newHash = this.calculateHash(newIndex, previousBlock.hash, newTimestamp, data);
        const newBlock = new Block(newIndex, previousBlock.hash, newTimestamp, data, newHash);
        this.chain.push(newBlock);
    }
}

module.exports = Blockchain;
