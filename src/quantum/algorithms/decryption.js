const { Lattice, KeyPair, Ciphertext, Plaintext } = require('node-lattice');

/**
 * Decrypts a message using lattice-based encryption
 * @param {Ciphertext} ciphertext - The encrypted message
 * @param {KeyPair} keyPair - The key pair containing the private key
 * @returns {string} - The decrypted message
 */
function decrypt(ciphertext, privateKey) {
    const lattice = new Lattice();
    const plaintext = lattice.decrypt(ciphertext, privateKey);
    return plaintext.toString();
}

/**
 * Example usage of the decryption function
 */
function main() {
    // Generate a key pair
    const lattice = new Lattice();
    const keyPair = lattice.generateKeyPair();

    // Example encrypted message (this should be obtained from the encryption process)
    const message = "This is a secret message!";
    const plaintext = new Plaintext(message);
    const encryptedMessage = lattice.encrypt(plaintext, keyPair.publicKey);

    console.log("Encrypted Message:", encryptedMessage);

    // Decrypt the message
    const decryptedMessage = decrypt(encryptedMessage, keyPair.privateKey);
    console.log("Decrypted Message:", decryptedMessage);
}

// Run the example
main();

module.exports = {
    decrypt
};
