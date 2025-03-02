// Import required packages
const express = require('express');
const bodyParser = require('body-parser');
const StellarSdk = require('stellar-sdk');
const dotenv = require('dotenv');

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
const piCoinAsset = new StellarSdk.Asset(process.env.PI_COIN_ASSET_CODE || 'PiCoin', process.env.PI_COIN_ISSUER || 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'); // Replace with actual issuer address

// Endpoint to get the balance of an account
app.get('/balance/:address', async (req, res) => {
    try {
        const account = await server.loadAccount(req.params.address);
        const balance = account.balances.find(b => b.asset_code === piCoinAsset.getCode());
        res.json({ balance: balance ? balance.balance : 0 });
    } catch (error) {
        console.error('Error fetching balance:', error);
        res.status(500).json({ error: 'Failed to fetch balance. ' + error.message });
    }
});

// Endpoint to send Pi Coin
app.post('/send', async (req, res) => {
    const { from, to, amount, secret } = req.body;

    try {
        const sourceKeypair = StellarSdk.Keypair.fromSecret(secret);
        const account = await server.loadAccount(sourceKeypair.publicKey());

        const transaction = new StellarSdk.TransactionBuilder(account, {
            fee: StellarSdk.BASE_FEE,
            networkPassphrase: StellarSdk.Networks.TESTNET,
        })
            .addOperation(StellarSdk.Operation.payment({
                destination: to,
                asset: piCoinAsset,
                amount: amount.toString(),
            }))
            .setTimeout(30)
            .build();

        transaction.sign(sourceKeypair);
        const result = await server.submitTransaction(transaction);
        res.json({ transactionHash: result.hash });
    } catch (error) {
        console.error('Error sending Pi Coin:', error);
        res.status(500).json({ error: 'Failed to send Pi Coin. ' + error.message });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
