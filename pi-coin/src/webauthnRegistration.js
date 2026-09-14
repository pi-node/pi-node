// Function to generate a random Uint8Array
function generateRandomBytes(length) {
    const randomBytes = new Uint8Array(length);
    window.crypto.getRandomValues(randomBytes);
    return randomBytes;
}

// Function to register biometric credentials
async function registerBiometric() {
    try {
        const userId = generateRandomBytes(16); // Generate a unique user ID
        const challenge = generateRandomBytes(32); // Generate a random challenge

        const publicKey = {
            challenge: challenge,
            rp: { name: "Pi Network" },
            user: {
                id: userId,
                name: "user@example.com",
                displayName: "User "
            },
            pubKeyCredParams: [{ type: "public-key", alg: -7 }], // ECDSA
            authenticatorSelection: {
                authenticatorAttachment: "platform", // Use platform authenticator (e.g., fingerprint)
                userVerification: "preferred" // User verification is preferred
            },
            timeout: 60000, // Set a timeout for the registration process
            excludeCredentials: [] // Optionally exclude existing credentials
        };

        const credential = await navigator.credentials.create({ publicKey });

        // Store credential.id and credential.response securely
        // For demonstration, we will log them to the console
        console.log("Credential ID:", credential.id);
        console.log("Credential Response:", credential.response);

        // Here you would typically send the credential to your server for storage
        // Example: await saveCredentialToServer(credential);

    } catch (error) {
        console.error("Error during registration:", error);
        alert("Registration failed: " + error.message);
    }
}

// Example function to save credential to server (stub)
async function saveCredentialToServer(credential) {
    // Implement your server-side logic to store the credential
    // This could involve sending the credential to your backend API
}
