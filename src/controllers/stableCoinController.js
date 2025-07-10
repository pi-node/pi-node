// Import required packages
const StellarSdk = require('stellar-sdk');
const config = require('../config/quantumConfig'); // Adjust the path as necessary

// Initialize Stellar SDK
const server = new StellarSdk.Server(config.service.endpoint);

// Pi Coin asset configuration
const piCoinAsset = new StellarSdk.Asset(config.piCoin.assetCode, config.piCoin.issuer);

// Controller for StableCoin operations
const stableCoinController = {
    // Get balance of an account
    getBalance: async (req, res) => {
        try {
            const account = await server.loadAccount(req.params.address);
            const balance = account.balances.find(b => b.asset_code === piCoinAsset.getCode());
            res.json({ balance: balance ? balance.balance : 0 });
        } catch (error) {
            console.error('Error fetching balance:', error);
            res.status(500).json({ error: 'Failed to fetch balance. ' + error.message });
        }
    },

    // Send Pi Coin from one account to another
    sendPiCoin: async (req, res) => {
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
    },
};

module.exports = stableCoinController;
