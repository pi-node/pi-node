// src/utils/consensus.js

const StellarSdk = require('stellar-sdk');
const config = require('../main/config');

class Consensus {
    constructor() {
        this.server = new StellarSdk.Server(config.STELLAR_HORIZON_URL);
        this.networkPassphrase = StellarSdk.Networks.TESTNET; // Change to NETWORKS.PUBLIC for mainnet
    }

    async getAccountDetails(accountId) {
        try {
            const account = await this.server.loadAccount(accountId);
            return account;
        } catch (error) {
            console.error('Error loading account:', error);
            throw new Error('Account not found or network error');
        }
    }

    async createTransaction(sourceSecret, operations) {
        const sourceKeypair = StellarSdk.Keypair.fromSecret(sourceSecret);
        const account = await this.getAccountDetails(sourceKeypair.publicKey());

        const transaction = new StellarSdk.TransactionBuilder(account, {
            fee: await this.server.fetchBaseFee(),
            networkPassphrase: this.networkPassphrase,
        })
            .addOperations(operations)
            .setTimeout(30)
            .build();

        transaction.sign(sourceKeypair);
        return transaction;
    }

    async submitTransaction(transaction) {
        try {
            const result = await this.server.submitTransaction(transaction);
            console.log('Transaction successful:', result);
            return result;
        } catch (error) {
            console.error('Transaction submission failed:', error);
            throw new Error('Transaction submission failed');
        }
    }

    async waitForTransaction(transactionId) {
        try {
            const result = await this.server.transactions().get(transactionId);
            return result;
        } catch (error) {
            console.error('Error fetching transaction:', error);
            throw new Error('Transaction not found or network error');
        }
    }

    async getTransactionStatus(transactionId) {
        try {
            const transaction = await this.waitForTransaction(transactionId);
            return transaction.status;
        } catch (error) {
            console.error('Error getting transaction status:', error);
            throw new Error('Could not retrieve transaction status');
        }
    }

    async getLatestLedger() {
        try {
            const ledger = await this.server.ledgers().order('desc').limit(1).call();
            return ledger.records[0];
        } catch (error) {
            console.error('Error fetching latest ledger:', error);
            throw new Error('Could not retrieve latest ledger');
        }
    }

    async getQuorumSlices(accountId) {
        try {
            const account = await this.getAccountDetails(accountId);
            return account.signers; // This will return the signers for multi-signature accounts
        } catch (error) {
            console.error('Error fetching quorum slices:', error);
            throw new Error('Could not retrieve quorum slices');
        }
    }
}

module.exports = new Consensus();
