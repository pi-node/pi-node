// src/index.js
const Blockchain = require('./blockchain');
const Transaction = require('./transaction');
const UserManager = require('./user').User Manager;
const SmartContract = require('./smartContract');
const PI_COIN = require('./constant');

// Initialize the blockchain and user manager
const blockchain = new Blockchain();
const userManager = new UserManager();

// Example users
const users = [
    { username: 'Alice', password: 'securePassword123' },
    { username: 'Bob', password: 'anotherSecurePassword456' }
];

// Register users
users.forEach(user => {
    try {
        userManager.registerUser (user.username, user.password);
    } catch (error) {
        console.error(`Error registering user ${user.username}: ${error.message}`);
    }
});

// Authenticate a user
let authenticatedUser ;
try {
    authenticatedUser  = userManager.authenticateUser ('Alice', 'securePassword123');
    console.log(`User  authenticated: ${authenticatedUser .username}`);
} catch (error) {
    console.error(`Authentication failed: ${error.message}`);
}

// Create a transaction
let transaction;
try {
    transaction = new Transaction(authenticatedUser .username, 'Bob', 100);
    transaction.validate(); // Validate the transaction
    blockchain.addTransaction(transaction); // Add transaction to the blockchain
    console.log(`Transaction created: ${transaction.transactionId}`);
} catch (error) {
    console.error(`Transaction error: ${error.message}`);
}

// Mine a block
try {
    blockchain.mineBlock(authenticatedUser .walletAddress); // Mine a block and reward the miner
    console.log("Block mined successfully!");
} catch (error) {
    console.error(`Mining error: ${error.message}`);
}

// Create and execute a smart contract
const contractData = { terms: "Alice pays Bob 100 PI" };
const smartContract = new SmartContract(contractData);

// Listen for execution events
smartContract.on('executed', (event) => {
    console.log("Smart contract executed event:", event);
});

// Execute the smart contract
try {
    smartContract.execute({ requiredField: "Some data" });
    console.log("Execution history:", smartContract.getExecutionHistory());
} catch (error) {
    console.error(`Smart contract execution error: ${error.message}`);
}

// Validate the blockchain
const isValidChain = blockchain.validateChain();
console.log(`Is blockchain valid? ${isValidChain}`);

module.exports = {
    blockchain,
    userManager,
    SmartContract,
};
