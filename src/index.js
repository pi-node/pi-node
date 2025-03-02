// Import required packages
const express = require('express');
const bodyParser = require('body-parser');
const Web3 = require('web3');
const StableCoinABI = require('./abis/StableCoin.json'); // Import the ABI of the StableCoin contract
const PriceFeedABI = require('./abis/PriceFeed.json'); // Import the ABI of the PriceFeed contract

// Initialize Express app
const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());

// Connect to Ethereum network (e.g., Ganache, Infura, etc.)
const web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545')); // Change to your provider

// Set contract addresses (replace with your deployed contract addresses)
const stableCoinAddress = '0xYourStableCoinAddress'; // Replace with actual StableCoin contract address
const priceFeedAddress = '0xYourPriceFeedAddress'; // Replace with actual PriceFeed contract address

// Create contract instances
const stableCoinContract = new web3.eth.Contract(StableCoinABI, stableCoinAddress);
const priceFeedContract = new web3.eth.Contract(PriceFeedABI, priceFeedAddress);

// Endpoint to get the balance of an account
app.get('/balance/:address', async (req, res) => {
    try {
        const balance = await stableCoinContract.methods.balanceOf(req.params.address).call();
        res.json({ balance: balance });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Endpoint to transfer tokens
app.post('/transfer', async (req, res) => {
    const { from, to, amount } = req.body;

    try {
        const accounts = await web3.eth.getAccounts();
        const result = await stableCoinContract.methods.transfer(to, amount).send({ from: from });
        res.json({ transactionHash: result.transactionHash });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Endpoint to adjust supply based on market conditions
app.post('/adjust-supply', async (req, res) => {
    const { owner } = req.body;

    try {
        const accounts = await web3.eth.getAccounts();
        const result = await stableCoinContract.methods.adjustSupply().send({ from: owner });
        res.json({ transactionHash: result.transactionHash });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
