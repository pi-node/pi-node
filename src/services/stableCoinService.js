// src/services/stableCoinService.js

const StellarSdk = require('stellar-sdk');
const { createTransaction } = require('../models/transactionModel'); // Import the transaction model

class StableCoinService {
    constructor(server, piCoinAsset) {
        this.server = server;
        this.piCoinAsset = piCoinAsset;
    }

    // Get the balance of a specific account
    async getBalance(address) {
        try {
            const account = await this.server.loadAccount(address);
            const balance = account.balances.find(b => b.asset_code === this.piCoinAsset.getCode());
            return balance ? balance.balance : 0;
        } catch (error) {
            throw new Error('Failed to fetch balance: ' + error.message);
        }
    }

    // Send Pi Coin from one account to another
    async sendPiCoin(from, to, amount, secret) {
        try {
            const sourceKeypair = StellarSdk.Keypair.fromSecret(secret);
            const account = await this.server.loadAccount(sourceKeypair.publicKey());

            const transaction = new StellarSdk.TransactionBuilder(account, {
                fee: StellarSdk.BASE_FEE,
                networkPassphrase: StellarSdk.Networks.TESTNET,
            })
                .addOperation(StellarSdk.Operation.payment({
                    destination: to,
                    asset: this.piCoinAsset,
                    amount: amount.toString(),
                }))
                .setTimeout(30)
                .build();

            transaction.sign(sourceKeypair);
            const result = await this.server.submitTransaction(transaction);

            // Log the transaction in the model
            createTransaction(from, to, amount, this.piCoinAsset.getCode(), result.hash);

            return result.hash; // Return the transaction hash
        } catch (error) {
            throw new Error('Failed to send Pi Coin: ' + error.message);
        }
    }
}

module.exports = StableCoinService;
