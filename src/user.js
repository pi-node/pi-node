// src/user.js
const bcrypt = require('bcrypt');

class User {
    constructor(username, password) {
        this.username = username;
        this.passwordHash = this.hashPassword(password);
    }

    hashPassword(password) {
        return bcrypt.hashSync(password, 10);
    }

    validatePassword(password) {
        return bcrypt.compareSync(password, this.passwordHash);
    }
}

module.exports = User;
