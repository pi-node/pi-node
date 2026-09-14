// scripts/stablecoinManager.js

const StellarSdk = require('stellar-sdk');
const dotenv = require('dotenv');

// Load environment variables from .env file
dotenv.config();

// Configure Stellar SDK
StellarSdk.Network.useTestNetwork(); // Use Test Network for testing
const server = new StellarSdk.Server(process.env.STELLAR_HORIZON_URL || 'https://horizon-testnet.stellar.org');

// Replace with your secret key
const issuerSecret = process.env.ISSUER_SECRET; // Issuer's secret key
const issuerKeypair = StellarSdk.Keypair.fromSecret(issuerSecret);
const assetCode = 'PiCoin'; // Your stablecoin asset code
const assetIssuer = issuerKeypair.publicKey(); // Issuer's public key

// Create a new asset
const stableCoinAsset = new StellarSdk.Asset(assetCode, assetIssuer);

// Function to create a trustline
async function createTrustline(account, asset) {
    const accountData = await server.loadAccount(account);
    const transaction = new StellarSdk.TransactionBuilder(accountData, {
        fee: StellarSdk.BASE_FEE,
        networkPassphrase: StellarSdk.Networks.TESTNET,
    })
    .addOperation(StellarSdk.Operation.changeTrust({
        asset: asset,
    }))
    .setTimeout(30)
    .build();

    transaction.sign(account); // Sign the transaction with the user's keypair
    await server.submitTransaction(transaction);
    console.log(`Trustline created for asset: ${assetCode}`);
}

// Function to issue the stablecoin
async function issueStableCoin(recipient, amount) {
    const accountData = await server.loadAccount(issuerKeypair.publicKey());
    const transaction = new StellarSdk.TransactionBuilder(accountData, {
        fee: StellarSdk.BASE_FEE,
        networkPassphrase: StellarSdk.Networks.TESTNET,
    })
    .addOperation(StellarSdk.Operation.payment({
        destination: recipient,
        asset: stableCoinAsset,
        amount: amount.toString(),
    }))
    .setTimeout(30)
    .build();

    transaction.sign(issuerKeypair); // Sign the transaction with the issuer's keypair
    await server.submitTransaction(transaction);
    console.log(`Issued ${amount} ${assetCode} to ${recipient}`);
}

// Function to burn the stablecoin
async function burnStableCoin(amount) {
    const accountData = await server.loadAccount(issuerKeypair.publicKey());
    const transaction = new StellarSdk.TransactionBuilder(accountData, {
        fee: StellarSdk.BASE_FEE,
        networkPassphrase: StellarSdk.Networks.TESTNET,
    })
    .addOperation(StellarSdk.Operation.payment({
        destination: StellarSdk.StrKey.encodeEd25519PublicKey(StellarSdk.Keypair.fromSecret(issuerSecret).publicKey()), // Burn to issuer's account
        asset: stableCoinAsset,
        amount: amount.toString(),
    }))
    .setTimeout(30)
    .build();

    transaction.sign(issuerKeypair); // Sign the transaction with the issuer's keypair
    await server.submitTransaction(transaction);
    console.log(`Burned ${amount} ${assetCode}`);
}

// Main function to run the script
async function main() {
    const recipient = process.env.RECIPIENT_PUBLIC_KEY; // Replace with the recipient's public key
    const amountToIssue = '1000'; // Amount to issue

    // Create trustline for the recipient
    await createTrustline(StellarSdk.Keypair.fromSecret(process.env.RECIPIENT_SECRET), stableCoinAsset);
    
    // Issue stablecoin to the recipient
    await issueStableCoin(recipient, amountToIssue);

    // Example of burning stablecoin
    // await burnStableCoin('500'); // Uncomment to burn 500 tokens
}

main().catch(console.error);
