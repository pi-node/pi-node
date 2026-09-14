const crypto = require('crypto');

class SupernodeEncryption {
  constructor() {
    this.algorithm = 'aes-256-cbc';
    this.password = 'your_secret_password';
  }

  async encrypt(data) {
    const cipher = crypto.createCipher(this.algorithm, this.password);
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
  }

  async decrypt(encrypted) {
    const decipher = crypto.createDecipher(this.algorithm, this.password);
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  }
}

module.exports = SupernodeEncryption;
