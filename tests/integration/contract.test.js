// tests/integration/contract.test.js

const StellarSdk = require('stellar-sdk');
const { createTransaction } = require('../../src/models/transactionModel'); // Import the transaction model
const StableCoinService = require('../../src/services/stableCoinService');

describe('Contract Integration Tests', () => {
    let stableCoinService;
    let mockServer;
    let mockAsset;

    beforeEach(() => {
        mockServer = {
            loadAccount: jest.fn(),
            submitTransaction: jest.fn(),
        };
        mockAsset = new StellarSdk.Asset('PiCoin', 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
        stableCoinService = new StableCoinService(mockServer, mockAsset);
    });

    test('should create and log a transaction when sending PiCoin', async () => {
        const mockAccount = {
            balances: [
                { asset_code: 'PiCoin', balance: '100' },
            ],
        };
        mockServer.loadAccount.mockResolvedValue(mockAccount);
        const mockTransaction = { hash: 'mockTransactionHash' };
        mockServer.submitTransaction.mockResolvedValue(mockTransaction);

        const transactionHash = await stableCoinService.sendPiCoin(
            'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'GYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
            '10',
            'SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        );

        expect(transactionHash).toBe('mockTransactionHash');
        const transaction = createTransaction('GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'GYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', '10', 'PiCoin', transactionHash);
        expect(transaction).toHaveProperty('id');
        expect(transaction).toHaveProperty('from', 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
        expect(transaction).toHaveProperty('to', 'GYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY');
    });
});
