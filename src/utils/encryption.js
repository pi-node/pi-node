// src/utils/encryption.js

const crypto = require('crypto');
const config = require('../main/config');

class Encryption {
    constructor() {
        this.algorithm = 'aes-256-cbc'; // AES encryption algorithm
        this.key = crypto.scryptSync(config.ENCRYPTION_SECRET_KEY, 'salt', 32); // Derive a key from the secret
        this.ivLength = 16; // Length of the initialization vector
    }

    // Encrypts a given text or JSON object
    encrypt(data) {
        try {
            const iv = crypto.randomBytes(this.ivLength); // Generate a random IV
            const cipher = crypto.createCipheriv(this.algorithm, this.key, iv);
            let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
            encrypted += cipher.final('hex');
            return {
                iv: iv.toString('hex'), // Return IV as hex
                encryptedData: encrypted, // Return encrypted data
            };
        } catch (error) {
            console.error('Encryption failed:', error);
            throw new Error('Encryption error');
        }
    }

    // Decrypts the encrypted data
    decrypt(encryptedData) {
        try {
            const iv = Buffer.from(encryptedData.iv, 'hex'); // Convert IV from hex to buffer
            const decipher = crypto.createDecipheriv(this.algorithm, this.key, iv);
            let decrypted = decipher.update(encryptedData.encryptedData, 'hex', 'utf8');
            decrypted += decipher.final('utf8');
            return JSON.parse(decrypted); // Return decrypted data as JSON
        } catch (error) {
            console.error('Decryption failed:', error);
            throw new Error('Decryption error');
        }
    }
}

module.exports = new Encryption();
