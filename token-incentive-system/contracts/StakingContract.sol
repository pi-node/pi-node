// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract StakingContract is Ownable, ReentrancyGuard {
    IERC20 public rewardToken; // The token that users will earn as rewards
    uint256 public rewardRate; // Reward rate in tokens per second
    uint256 public totalStaked; // Total amount of tokens staked

    struct Stake {
        uint256 amount; // Amount of tokens staked
        uint256 lastRewardTime; // Last time rewards were calculated
        uint256 rewards; // Accumulated rewards
    }

    mapping(address => Stake) private stakes; // Mapping of user stakes

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardPaid(address indexed user, uint256 reward);
    event RewardRateChanged(uint256 newRate);
    event EmergencyWithdraw(address indexed user, uint256 amount);

    constructor(IERC20 _rewardToken, uint256 _rewardRate) {
        rewardToken = _rewardToken;
        rewardRate = _rewardRate;
    }

    // Function to stake tokens
    function stake(uint256 amount) external nonReentrant {
        require(amount > 0, "Cannot stake 0");
        require(rewardToken.balanceOf(msg.sender) >= amount, "Insufficient balance");

        // Update rewards before staking
        _updateRewards(msg.sender);

        // Transfer tokens from user to contract
        rewardToken.transferFrom(msg.sender, address(this), amount);
        stakes[msg.sender].amount += amount;
        totalStaked += amount;

        emit Staked(msg.sender, amount);
    }

    // Function to unstake tokens and claim rewards
    function unstake() external nonReentrant {
        Stake storage userStake = stakes[msg.sender];
        require(userStake.amount > 0, "No tokens staked");

        // Update rewards before unstaking
        _updateRewards(msg.sender);

        uint256 amountToUnstake = userStake.amount;
        userStake.amount = 0; // Reset the user's stake
        totalStaked -= amountToUnstake;

        // Transfer staked tokens back to user
        rewardToken.transfer(msg.sender, amountToUnstake);
        // Pay out rewards
        uint256 reward = userStake.rewards;
        userStake.rewards = 0; // Reset rewards after payout
        rewardToken.transfer(msg.sender, reward);

        emit Unstaked(msg.sender, amountToUnstake);
        emit RewardPaid(msg.sender, reward);
    }

    // Function to update rewards for a user
    function _updateRewards(address user) internal {
        Stake storage userStake = stakes[user];
        if (userStake.amount > 0) {
            uint256 timeElapsed = block.timestamp - userStake.lastRewardTime;
            userStake.rewards += (userStake.amount * rewardRate * timeElapsed) / 1e18;
        }
        userStake.lastRewardTime = block.timestamp; // Update last reward time
    }

    // Function to get the staking balance of a user
    function stakingBalance(address user) external view returns (uint256) {
        return stakes[user].amount;
    }

    // Function to get the total staked amount
    function totalStakedAmount() external view returns (uint256) {
        return totalStaked;
    }

    // Function to change the reward rate (only owner)
    function setRewardRate(uint256 newRate) external onlyOwner {
        _updateRewards(msg.sender); // Update rewards before changing the rate
        rewardRate = newRate;
        emit RewardRateChanged(newRate);
    }

    // Emergency withdraw function (without rewards)
    function emergencyWithdraw(uint256 amount) external nonReentrant {
        Stake storage userStake = stakes[msg.sender];
        require(amount > 0, "Cannot withdraw 0");
        require(userStake.amount >= amount, "Insufficient staked balance");

        // Update the user's stake
        userStake.amount -= amount;
        totalStaked -= amount;

        // Transfer tokens back to user
        rewardToken.transfer(msg.sender, amount);

        emit EmergencyWithdraw(msg.sender, amount);
    }
}
