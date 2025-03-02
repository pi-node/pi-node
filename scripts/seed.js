// scripts/seed.js

const StellarSdk = require('stellar-sdk');
const { createUser } = require('../src/models/userModel'); // Adjust the path as necessary
const { createTransaction } = require('../src/models/transactionModel'); // Adjust the path as necessary
const dotenv = require('dotenv');

// Load environment variables from .env file
dotenv.config();

// Function to create initial users
const seedUsers = () => {
    const users = [
        { stellarAddress: 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', username: 'User1' },
        { stellarAddress: 'GYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', username: 'User2' },
    ];

    users.forEach(user => {
        const newUser = createUser(user.stellarAddress, user.username);
        console.log(`Created user: ${newUser.username} with address: ${newUser.stellarAddress}`);
    });
};

// Function to create initial transactions
const seedTransactions = () => {
    const transactions = [
        { from: 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', to: 'GYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', amount: '10', assetCode: 'PiCoin', transactionHash: 'mockTransactionHash1' },
        { from: 'GYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', to: 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', amount: '5', assetCode: 'PiCoin', transactionHash: 'mockTransactionHash2' },
    ];

    transactions.forEach(transaction => {
        const newTransaction = createTransaction(transaction.from, transaction.to, transaction.amount, transaction.assetCode, transaction.transactionHash);
        console.log(`Created transaction from: ${newTransaction.from} to: ${newTransaction.to} with amount: ${newTransaction.amount}`);
    });
};

// Main function to seed data
const main = async () => {
    console.log('Seeding initial data...');
    seedUsers();
    seedTransactions();
    console.log('Seeding completed successfully.');
};

main();
