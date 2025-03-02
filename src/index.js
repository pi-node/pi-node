// Import required packages
const express = require('express');
const bodyParser = require('body-parser');
const StellarSdk = require('stellar-sdk');
const dotenv = require('dotenv');
const routes = require('./routes'); // Import routes

// Load environment variables from .env file
dotenv.config();

// Initialize Express app
const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());

// Configure Stellar SDK
StellarSdk.Network.useTestNetwork(); // Use Test Network
const server = new StellarSdk.Server(process.env.STELLAR_HORIZON_URL || 'https://horizon-testnet.stellar.org'); // Default to Stellar Testnet

// Pi Coin configuration
const piCoinAsset = new StellarSdk.Asset(
    process.env.PI_COIN_ASSET_CODE || 'PiCoin',
    process.env.PI_COIN_ISSUER || 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' // Replace with actual issuer address
);

// Middleware to attach Stellar server and Pi Coin asset to the request
app.use((req, res, next) => {
    req.stellarServer = server;
    req.piCoinAsset = piCoinAsset;
    next();
});

// Use the routes
app.use(routes);

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
