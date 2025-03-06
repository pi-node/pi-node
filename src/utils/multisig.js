// src/utils/multisig.js

const StellarSdk = require('stellar-sdk');
const config = require('../main/config');

class MultiSig {
    constructor() {
        this.server = new StellarSdk.Server(config.STELLAR_HORIZON_URL);
        this.networkPassphrase = StellarSdk.Networks.TESTNET; // Change to NETWORKS.PUBLIC for mainnet
    }

    // Create a multi-signature account
    async createMultiSigAccount(secretKey, signers, threshold) {
        const keypair = StellarSdk.Keypair.fromSecret(secretKey);
        const account = await this.server.loadAccount(keypair.publicKey());

        const transaction = new StellarSdk.TransactionBuilder(account, {
            fee: await this.server.fetchBaseFee(),
            networkPassphrase: this.networkPassphrase,
        })
            .addOperation(StellarSdk.Operation.setOptions({
                masterWeight: threshold,
                lowThreshold: threshold,
                medThreshold: threshold,
                highThreshold: threshold,
                signer: signers.map(signer => ({
                    ed25519PublicKey: signer.publicKey,
                    weight: signer.weight,
                })),
            }))
            .setTimeout(30)
            .build();

        transaction.sign(keypair);
        return await this.submitTransaction(transaction);
    }

    // Add a signer to an existing multi-signature account
    async addSigner(secretKey, newSigner, newWeight) {
        const keypair = StellarSdk.Keypair.fromSecret(secretKey);
        const account = await this.server.loadAccount(keypair.publicKey());

        const transaction = new StellarSdk.TransactionBuilder(account, {
            fee: await this.server.fetchBaseFee(),
            networkPassphrase: this.networkPassphrase,
        })
            .addOperation(StellarSdk.Operation.setOptions({
                signer: {
                    ed25519PublicKey: newSigner,
                    weight: newWeight,
                },
            }))
            .setTimeout(30)
            .build();

        transaction.sign(keypair);
        return await this.submitTransaction(transaction);
    }

    // Remove a signer from an existing multi-signature account
    async removeSigner(secretKey, signerToRemove) {
        const keypair = StellarSdk.Keypair.fromSecret(secretKey);
        const account = await this.server.loadAccount(keypair.publicKey());

        const transaction = new StellarSdk.TransactionBuilder(account, {
            fee: await this.server.fetchBaseFee(),
            networkPassphrase: this.networkPassphrase,
        })
            .addOperation(StellarSdk.Operation.setOptions({
                signer: {
                    ed25519PublicKey: signerToRemove,
                    weight: 0, // Set weight to 0 to remove the signer
                },
            }))
            .setTimeout(30)
            .build();

        transaction.sign(keypair);
        return await this.submitTransaction(transaction);
    }

    // Submit a transaction to the Stellar network
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

    // Validate a transaction against the required signatures
    async validateTransaction(transactionId) {
        try {
            const transaction = await this.server.transactions().get(transactionId);
            const requiredSignatures = transaction.signatures.length;
            const actualSignatures = transaction.signatures.filter(sig => sig).length;

            return {
                transactionId,
                requiredSignatures,
                actualSignatures,
                isValid: actualSignatures >= requiredSignatures,
            };
        } catch (error) {
            console.error('Error validating transaction:', error);
            throw new Error('Transaction validation failed');
        }
    }
}

module.exports = new MultiSig();
