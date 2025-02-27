// src/index.js
const Blockchain = require('./blockchain');
const Transaction = require('./transaction');
const User = require('./user');
const SmartContract = require('./smartContract');
const PI_COIN = require('./constant');

const blockchain = new Blockchain();

// Example usage
constnewTransaction = new Transaction("Alice", "Bob", 100);
blockchain.addBlock(newTransaction);

const user = new User("Alice", "securePassword123");
console.log("User created:", user.username);

const contract = new SmartContract({ terms: "Alice pays Bob 100 PI" });
contract.execute();

console.log("Current blockchain:", JSON.stringify(blockchain, null, 2));
