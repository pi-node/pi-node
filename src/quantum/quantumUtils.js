const crypto = require('crypto');

/**
 * Generates a random key for encryption
 * @param {number} length - Length of the key in bytes
 * @returns {string} - Randomly generated key in hexadecimal format
 */
function generateRandomKey(length) {
    return crypto.randomBytes(length).toString('hex');
}

/**
 * Encodes a message to a binary format
 * @param {string} message - The message to encode
 * @returns {string} - The encoded message in binary format
 */
function encodeMessageToBinary(message) {
    return message.split('').map(char => {
        return char.charCodeAt(0).toString(2).padStart(8, '0');
    }).join(' ');
}

/**
 * Decodes a binary message back to a string
 * @param {string} binaryMessage - The binary message to decode
 * @returns {string} - The decoded message
 */
function decodeBinaryToMessage(binaryMessage) {
    return binaryMessage.split(' ').map(bin => {
        return String.fromCharCode(parseInt(bin, 2));
    }).join('');
}

/**
 * Hashes a message using SHA-256
 * @param {string} message - The message to hash
 * @returns {string} - The hashed message in hexadecimal format
 */
function hashMessage(message) {
    return crypto.createHash('sha256').update(message).digest('hex');
}

/**
 * Example usage of utility functions
 */
function main() {
    const message = "This is a secret message!";
    
    // Generate a random key
    const key = generateRandomKey(32); // 256-bit key
    console.log("Generated Key:", key);
    
    // Encode the message to binary
    const binaryMessage = encodeMessageToBinary(message);
    console.log("Encoded Binary Message:", binaryMessage);
    
    // Decode the binary message back to string
    const decodedMessage = decodeBinaryToMessage(binaryMessage);
    console.log("Decoded Message:", decodedMessage);
    
    // Hash the message
    const hashedMessage = hashMessage(message);
    console.log("Hashed Message:", hashedMessage);
}

// Run the example
main();

module.exports = {
    generateRandomKey,
    encodeMessageToBinary,
    decodeBinaryToMessage,
    hashMessage
};
