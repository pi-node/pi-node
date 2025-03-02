// tests/unit/stableCoin.test.js

const StellarSdk = require('stellar-sdk');
const StableCoinService = require('../../src/services/stableCoinService');
const { createTransaction } = require('../../src/models/transactionModel');

// Mock the Stellar SDK
jest.mock('stellar-sdk');

describe('StableCoinService', () => {
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

    test('should get balance for a valid account', async () => {
        const mockAccount = {
            balances: [
                { asset_code: 'PiCoin', balance: '100' },
                { asset_code: 'XLM', balance: '50' },
            ],
        };
        mockServer.loadAccount.mockResolvedValue(mockAccount);

        const balance = await stableCoinService.getBalance('GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
        expect(balance).toBe('100');
    });

    test('should return 0 balance for an account without PiCoin', async () => {
        const mockAccount = {
            balances: [
                { asset_code: 'XLM', balance: '50' },
            ],
        };
        mockServer.loadAccount.mockResolvedValue(mockAccount);

        const balance = await stableCoinService.getBalance('GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
        expect(balance).toBe(0);
    });

    test('should send PiCoin and return transaction hash', async () => {
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
    });

    test('should throw an error if sending PiCoin fails', async () => {
        const mockAccount = {
            balances: [
                { asset_code: 'PiCoin', balance: '100' },
            ],
        };
        mockServer.loadAccount.mockResolvedValue(mockAccount);
        mockServer.submitTransaction.mockRejectedValue(new Error('Transaction failed'));

        await expect(stableCoinService.sendPiCoin(
            'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'GYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
            '10',
            'SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        )).rejects.toThrow('Failed to send Pi Coin: Transaction failed');
    });
});
