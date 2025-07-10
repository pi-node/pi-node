const { Lattice, KeyPair, Ciphertext, Plaintext } = require('node-lattice');

/**
 * Generates a key pair for encryption and decryption
 * @returns {KeyPair} - The generated key pair
 */
function generateKeyPair() {
    const lattice = new Lattice();
    return lattice.generateKeyPair();
}

/**
 * Encrypts a message using lattice-based encryption
 * @param {string} message - The message to encrypt
 * @param {KeyPair} keyPair - The key pair containing the public key
 * @returns {Ciphertext} - The encrypted message
 */
function encrypt(message, publicKey) {
    const lattice = new Lattice();
    const plaintext = new Plaintext(message);
    return lattice.encrypt(plaintext, publicKey);
}

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

// Example usage
const keyPair = generateKeyPair();
const message = "This is a secret message!";
const encryptedMessage = encrypt(message, keyPair.publicKey);
console.log("Encrypted Message:", encryptedMessage);

const decryptedMessage = decrypt(encryptedMessage, keyPair.privateKey);
console.log("Decrypted Message:", decryptedMessage);

module.exports = {
    generateKeyPair,
    encrypt,
    decrypt
};
