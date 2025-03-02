// src/user.js
const bcrypt = require('bcrypt');
const crypto = require('crypto');

class User {
    constructor(username, password) {
        this.username = username;
        this.passwordHash = this.hashPassword(password);
        this.walletAddress = this.generateWalletAddress();
    }

    // Hash the user's password
    hashPassword(password) {
        return bcrypt.hashSync(password, 10);
    }

    // Validate the user's password
    validatePassword(password) {
        return bcrypt.compareSync(password, this.passwordHash);
    }

    // Generate a unique wallet address
    generateWalletAddress() {
        return `0x${crypto.randomBytes(20).toString('hex')}`; // Generate a random wallet address
    }

    // Log user details (for debugging purposes)
    logUser Details() {
        console.log(`Username: ${this.username}`);
        console.log(`Wallet Address: ${this.walletAddress}`);
    }
}

// User management functions
class UserManager {
    constructor() {
        this.users = []; // In-memory user storage (replace with a database in production)
    }

    // Register a new user
    registerUser (username, password) {
        if (this.users.find(user => user.username === username)) {
            throw new Error("Username already exists.");
        }
        const newUser  = new User(username, password);
        this.users.push(newUser );
        console.log(`User  registered: ${username}`);
        return newUser ;
    }

    // Authenticate a user
    authenticateUser (username, password) {
        const user = this.users.find(user => user.username === username);
        if (!user || !user.validatePassword(password)) {
            throw new Error("Invalid username or password.");
        }
        console.log(`User  authenticated: ${username}`);
        return user;
    }

    // Get user details
    getUser (username) {
        const user = this.users.find(user => user.username === username);
        if (!user) {
            throw new Error("User  not found.");
        }
        return user;
    }
}

// Example usage
const userManager = new UserManager();

try {
    const user1 = userManager.registerUser ("Alice", "securePassword123");
    user1.logUser Details();

    const authenticatedUser  = userManager.authenticateUser ("Alice", "securePassword123");
    console.log("Authenticated User:", authenticatedUser .username);
} catch (error) {
    console.error(error.message);
}

module.exports = {
    User,
    UserManager,
};
