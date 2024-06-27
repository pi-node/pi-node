const crypto = require('crypto');

const encryptData = (data) => {
  const cipher = crypto.createCipher('aes-256-cbc', 'secretKey');
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return encrypted;
};

const decryptData = (encrypted) => {
  const decipher = crypto.createDecipher('aes-256-cbc', 'secretKey');
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
};
