const { Lattice, KeyPair, Ciphertext, Plaintext } = require('node-lattice');
const { generateKeyPair, encrypt } = require('./algorithms/encryption');
const { decrypt } = require('./algorithms/decryption');

/**
 * Represents a Quantum Node
 */
class QuantumNode {
    constructor() {
        this.keyPair = generateKeyPair(); // Generate a key pair for this node
    }

    /**
     * Encrypts a message
     * @param {string} message - The message to encrypt
     * @returns {Ciphertext} - The encrypted message
     */
    sendMessage(message) {
        console.log(`Sending message: ${message}`);
        const encryptedMessage = encrypt(message, this.keyPair.publicKey);
        console.log("Encrypted Message:", encryptedMessage);
        return encryptedMessage;
    }

    /**
     * Decrypts a received message
     * @param {Ciphertext} encryptedMessage - The encrypted message to decrypt
     * @returns {string} - The decrypted message
     */
    receiveMessage(encryptedMessage) {
        const decryptedMessage = decrypt(encryptedMessage, this.keyPair.privateKey);
        console.log("Decrypted Message:", decryptedMessage);
        return decryptedMessage;
    }
}

/**
 * Example usage of the QuantumNode
 */
function main() {
    const node = new QuantumNode();
    
    // Example message to send
    const message = "This is a secret message!";
    
    // Encrypt and send the message
    const encryptedMessage = node.sendMessage(message);
    
    // Decrypt the received message
    node.receiveMessage(encryptedMessage);
}

// Run the example
main();

module.exports = QuantumNode;
