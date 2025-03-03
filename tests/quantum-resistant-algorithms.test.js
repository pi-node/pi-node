// tests/quantum-resistant-algorithms.test.js
const {
    generateQuantumSecureKey,
    encryptMessage,
    decryptMessage,
    keyExchange,
} = require('../quantum/quantum-resistant-algorithms');

test('Generate a quantum secure key', () => {
    const key = generateQuantumSecureKey();
    expect(key).toHaveLength(64); // 32 bytes in hex
});

test('Encrypt and decrypt a message', () => {
    const { generateKeyPairSync } = require('crypto');
    const { publicKey, privateKey } = generateKeyPairSync('rsa', {
        modulusLength: 2048,
    });

    const message = 'Hello, Pi Coin!';
    const encryptedMessage = encryptMessage(message, publicKey);
    const decryptedMessage = decryptMessage(encryptedMessage, privateKey);

    expect(decryptedMessage).toBe(message);
});

test('Key exchange produces a shared secret', () => {
    const { generateKeyPairSync } = require('crypto');
    const { publicKey: publicKey1, privateKey: privateKey1 } = generateKeyPairSync('rsa', {
        modulusLength: 2048,
    });
    const { publicKey: publicKey2, privateKey: privateKey2 } = generateKeyPairSync('rsa', {
        modulusLength: 2048,
    });

    const sharedSecret = keyExchange(privateKey1, publicKey2);
    expect(sharedSecret).toBeDefined();
});
