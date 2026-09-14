const fs = require('fs');
const path = require('path');

// Load secrets
const secretsPath = path.join(__dirname, 'config', 'secrets.json');

try {
    const secrets = JSON.parse(fs.readFileSync(secretsPath, 'utf8'));

    // Example usage
    console.log("Encryption Secret Key:", secrets.encryption.secretKey);
    console.log("Service A API Key:", secrets.apiKeys.serviceA);
    console.log("Database Username:", secrets.database.username);
    console.log("JWT Secret:", secrets.jwt.secret);
    console.log("Payment Gateway API Key:", secrets.thirdPartyServices.paymentGateway.apiKey);
} catch (error) {
    console.error("Error reading secrets file:", error);
}
