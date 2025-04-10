// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Context.sol";

contract OracleIntegration is Context, Ownable {
    AggregatorV3Interface internal priceFeed;

    event PriceUpdated(int256 price);
    event Error(string message);

    constructor(address _priceFeedAddress) {
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    /**
     * @dev Returns the latest price of the asset in USD.
     */
    function getLatestPrice() public view returns (int256) {
        (
            uint80 roundID,
            int256 price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();

        if (timeStamp == 0) {
            emit Error("Price feed not available");
            return 0; // Return 0 if the price feed is not available
        }

        emit PriceUpdated(price);
        return price;
    }

    /**
     * @dev Allows the owner to update the price feed address.
     */
    function updatePriceFeed(address _newPriceFeedAddress) external onlyOwner {
        priceFeed = AggregatorV3Interface(_newPriceFeedAddress);
    }
}
