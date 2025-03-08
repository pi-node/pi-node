// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract TokenIncentive is ERC20, Ownable, ReentrancyGuard {
    // Mapping from user address to staking balance
    mapping(address => uint256) private _stakingBalances;
    // Mapping from user address to staking timestamp
    mapping(address => uint256) private _stakingTimestamps;
    // Total staked amount
    uint256 private _totalStaked;
    // Reward rate (in tokens per second)
    uint256 public rewardRate = 1e18; // 1 token per second

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardPaid(address indexed user, uint256 reward);
    event RewardRateChanged(uint256 newRate);

    constructor() ERC20("IncentiveToken", "ITK") {
        // Mint initial supply to the contract owner
        _mint(msg.sender, 1000000 * 10 ** decimals()); // 1 million tokens
    }

    // Function to stake tokens
    function stake(uint256 amount) external nonReentrant {
        require(amount > 0, "Cannot stake 0");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");

        // Transfer tokens from user to contract
        _transfer(msg.sender, address(this), amount);
        _stakingBalances[msg.sender] += amount;
        _stakingTimestamps[msg.sender] = block.timestamp;
        _totalStaked += amount;

        emit Staked(msg.sender, amount);
    }

    // Function to unstake tokens and claim rewards
    function unstake() external nonReentrant {
        uint256 stakedAmount = _stakingBalances[msg.sender];
        require(stakedAmount > 0, "No tokens staked");

        // Calculate reward
        uint256 reward = calculateReward(msg.sender);
        _stakingBalances[msg.sender] = 0;
        _totalStaked -= stakedAmount;

        // Transfer staked tokens back to user
        _transfer(address(this), msg.sender, stakedAmount);
        // Transfer reward tokens to user
        _mint(msg.sender, reward);

        emit Unstaked(msg.sender, stakedAmount);
        emit RewardPaid(msg.sender, reward);
    }

    // Function to calculate reward for a user
    function calculateReward(address user) public view returns (uint256) {
        uint256 stakedAmount = _stakingBalances[user];
        uint256 stakingDuration = block.timestamp - _stakingTimestamps[user];
        return (stakedAmount * stakingDuration * rewardRate) / 1e18;
    }

    // Function to get the staking balance of a user
    function stakingBalance(address user) external view returns (uint256) {
        return _stakingBalances[user];
    }

    // Function to get the total staked amount
    function totalStaked() external view returns (uint256) {
        return _totalStaked;
    }

    // Function to change the reward rate (only owner)
    function setRewardRate(uint256 newRate) external onlyOwner {
        rewardRate = newRate;
        emit RewardRateChanged(newRate);
    }

    // Emergency withdraw function (without rewards)
    function emergencyWithdraw(uint256 amount) external nonReentrant {
        require(amount > 0, "Cannot withdraw 0");
        require(_stakingBalances[msg.sender] >= amount, "Insufficient staked balance");

        // Update staking balance
        _stakingBalances[msg.sender] -= amount;
        _totalStaked -= amount;

        // Transfer tokens back to user
        _transfer(address(this), msg.sender, amount);
    }
}
