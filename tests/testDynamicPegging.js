// tests/testDynamicPegging.js

const { monitorPriceAndAdjustSupply } = require('../dynamicPegging');
const { mintTokens, burnTokens, getCurrentSupply } = require('./mocks/supplyManager');
const { getPriceFromOracle } = require('./mocks/oracleIntegration');

// Mocking the dependencies
jest.mock('./mocks/supplyManager');
jest.mock('./mocks/oracleIntegration');

describe('Dynamic Pegging Tests', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('should burn tokens when price is above target', async () => {
        // Arrange
        getPriceFromOracle.mockResolvedValue(320000); // Mock price above target
        getCurrentSupply.mockReturnValue(1000000000); // Mock current supply

        // Act
        await monitorPriceAndAdjustSupply();

        // Assert
        expect(burnTokens).toHaveBeenCalled();
        expect(mintTokens).not.toHaveBeenCalled();
    });

    test('should mint tokens when price is below target', async () => {
        // Arrange
        getPriceFromOracle.mockResolvedValue(310000); // Mock price below target
        getCurrentSupply.mockReturnValue(1000000000); // Mock current supply

        // Act
        await monitorPriceAndAdjustSupply();

        // Assert
        expect(mintTokens).toHaveBeenCalled();
        expect(burnTokens).not.toHaveBeenCalled();
    });

    test('should not adjust supply when price is within threshold', async () => {
        // Arrange
        getPriceFromOracle.mockResolvedValue(313000); // Mock price within threshold
        getCurrentSupply.mockReturnValue(1000000000); // Mock current supply

        // Act
        await monitorPriceAndAdjustSupply();

        // Assert
        expect(mintTokens).not.toHaveBeenCalled();
        expect(burnTokens).not.toHaveBeenCalled();
    });

    test('should handle errors gracefully', async () => {
        // Arrange
        getPriceFromOracle.mockRejectedValue(new Error('Oracle error')); // Mock error

        // Act
        await monitorPriceAndAdjustSupply();

        // Assert
        expect(burnTokens).not.toHaveBeenCalled();
        expect(mintTokens).not.toHaveBeenCalled();
    });
});
