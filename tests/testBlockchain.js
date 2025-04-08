const { expect } = require('chai');
const crypto = require('crypto');
const rsa = require('node-rsa');
const Blockchain = require('./blockchain'); // Assuming your blockchain code is in a file named blockchain.js

describe('Blockchain', function() {
    let blockchain;

    beforeEach(function() {
        blockchain = new Blockchain();
        blockchain.registerUser ("test_user", "test_password");
    });

    it('should register a user', function() {
        expect(blockchain.users).to.have.property("test_user");
        const hashedPassword = crypto.createHash('sha256').update("test_password").digest('hex');
        expect(blockchain.users["test_user"]).to.equal(hashedPassword);
    });

    it('should authenticate a user with correct credentials', function() {
        expect(blockchain.authenticateUser ("test_user", "test_password")).to.be.true;
    });

    it('should fail to authenticate a user with incorrect credentials', function() {
        expect(blockchain.authenticateUser ("test_user", "wrong_password")).to.be.false;
    });

    it('should sign and verify a transaction', function() {
        const key = new rsa({b: 512});
        const privateKey = key.exportKey('private');
        const publicKey = key.exportKey('public');
        const transaction = { sender: "Alice", recipient: "Bob", amount: 50.0 };
        const signature = blockchain.signTransaction(privateKey, transaction);

        expect(blockchain.verifySignature(publicKey, signature, transaction)).to.be.true;
    });

    it('should fail to verify an invalid signature', function() {
        const key = new rsa({b: 512});
        const privateKey = key.exportKey('private');
        const publicKey = key.exportKey('public');
        const transaction = { sender: "Alice", recipient: "Bob", amount: 50.0 };
        const signature = blockchain.signTransaction(privateKey, transaction);

        // Modify the transaction to create an invalid signature
        transaction.amount = 100.0;
        expect(blockchain.verifySignature(publicKey, signature, transaction)).to.be.false;
    });

    it('should add a valid transaction', function() {
        const key = new rsa({b: 512});
        const privateKey = key.exportKey('private');
        const publicKey = key.exportKey('public');
        const transaction = { sender: "Alice", recipient: "Bob", amount: 50.0 };
        const signature = blockchain.signTransaction(privateKey, transaction);

        blockchain.addTransaction(transaction.sender, transaction.recipient, transaction.amount, signature);
        expect(blockchain.currentTransactions).to.have.lengthOf(1);
    });

    it('should mine a new block', function() {
        const key = new rsa({b: 512});
        const privateKey = key.exportKey('private');
        const publicKey = key.exportKey('public');
        const transaction = { sender: "Alice", recipient: "Bob", amount: 50.0 };
        const signature = blockchain.signTransaction(privateKey, transaction);

        blockchain.addTransaction(transaction.sender, transaction.recipient, transaction.amount, signature);
        const newBlock = blockchain.mineBlock();

        expect(newBlock.index).to.equal(1);
        expect(newBlock.transactions).to.have.lengthOf(1);
    });

    it('should validate the blockchain', function() {
        expect(blockchain.validateChain()).to.be.true;

        // Tamper with the blockchain
        blockchain.chain[1].transactions[0].amount = 100.0;
        expect(blockchain.validateChain()).to.be.false;
    });

    it('should get the blockchain', function() {
        const chain = blockchain.getChain();
        expect(chain).to.have.lengthOf(1); // Only the genesis block should be present initially

        // Mine a block
        const key = new rsa({b: 512});
        const privateKey = key.exportKey('private');
        const publicKey = key.exportKey('public');
        const transaction = { sender: "Alice", recipient: "Bob", amount: 50.0 };
        const signature = blockchain.signTransaction(privateKey, transaction);
        blockchain.addTransaction(transaction.sender, transaction.recipient, transaction.amount, signature);
        blockchain.mineBlock();

        const updatedChain = blockchain.getChain();
        expect(updatedChain).to.have.lengthOf(2); // Now there should be the genesis block and one mined block
    });
});

// Run the tests
if (require.main === module) {
    require('mocha').run();
}
