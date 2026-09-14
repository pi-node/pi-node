const { Node } = require('./node');
const { crypto } = require('crypto');

class Security {
  constructor() {
    this.keys = {};
  }

  async generateKeyPair() {
    const { publicKey, privateKey } = await crypto.generateKeyPair('rsa', {
      modulusLength: 2048,
    });
    this.keys.publicKey = publicKey.export({ type: 'spki', format: 'pem' });
    this.keys.privateKey = privateKey.export({ type: 'pkcs8', format: 'pem' });
  }

  async encryptData(data) {
    const encryptedData = await crypto.publicEncrypt(
      {
        key: this.keys.publicKey,
padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: 'sha256',
      },
      Buffer.from(data)
    );
    return encryptedData.toString('base64');
  }

  async decryptData(encryptedData) {
    const decryptedData = await crypto.privateDecrypt(
      {
        key: this.keys.privateKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: 'sha256',
      },
      Buffer.from(encryptedData, 'base64')
    );
    return decryptedData.toString('utf8');
  }
}

module.exports = Security;
