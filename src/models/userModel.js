// src/models/userModel.js

class User {
    constructor(id, stellarAddress, username) {
        this.id = id; // Unique identifier for the user
        this.stellarAddress = stellarAddress; // Stellar account address
        this.username = username; // Username or display name
        this.createdAt = new Date(); // Timestamp of when the user was created
    }
}

// Example in-memory user storage (for demonstration purposes)
const users = [];

// Function to create a new user
const createUser  = (stellarAddress, username) => {
    const id = users.length + 1; // Simple ID generation
    const newUser  = new User(id, stellarAddress, username);
    users.push(newUser );
    return newUser ;
};

// Function to find a user by ID
const findUser ById = (id) => {
    return users.find(user => user.id === id);
};

// Function to find a user by Stellar address
const findUser ByStellarAddress = (stellarAddress) => {
    return users.find(user => user.stellarAddress === stellarAddress);
};

// Export the User model and functions
module.exports = {
    User,
    createUser ,
    findUser ById,
    findUser ByStellarAddress,
};
