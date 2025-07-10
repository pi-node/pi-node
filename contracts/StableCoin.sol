// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

interface IPriceFeed {
    function getLatestPrice() external view returns (uint256);
}

contract StableCoin is Ownable {
    using SafeMath for uint256;

    string public name = "Pi Coin";
    string public symbol = "Pi";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    uint256 public constant STABLE_VALUE = 314159 * 10 ** 18; // $314,159 in wei
    uint256 public constant TOTAL_SUPPLY_CAP = 100000000000 * 10 ** 18; // 100 billion tokens
    IPriceFeed public priceFeed; // Price feed contract

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event ValueAdjusted(uint256 newValue);
    event TokensMinted(address indexed to, uint256 amount);
    event TokensBurned(address indexed from, uint256 amount);

    constructor(address _priceFeed) {
        require(_priceFeed != address(0), "Invalid price feed address");
        priceFeed = IPriceFeed(_priceFeed);
        totalSupply = 0; // Start with zero total supply
    }

    // Function to transfer tokens
    function transfer(address to, uint256 amount) external returns (bool) {
        require(to != address(0), "Invalid address");
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");

        balanceOf[msg.sender] = balanceOf[msg.sender].sub(amount);
        balanceOf[to] = balanceOf[to].add(amount);
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    // Function to approve token spending
    function approve(address spender, uint256 amount) external returns (bool) {
        require(spender != address(0), "Invalid address");
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    // Function to transfer tokens on behalf of another address
    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        require(from != address(0), "Invalid address");
        require(to != address(0), "Invalid address");
        require(balanceOf[from] >= amount, "Insufficient balance");
        require(allowance[from][msg.sender] >= amount, "Allowance exceeded");

        balanceOf[from] = balanceOf[from].sub(amount);
        balanceOf[to] = balanceOf[to].add(amount);
        allowance[from][msg.sender] = allowance[from][msg.sender].sub(amount);
        emit Transfer(from, to, amount);
        return true;
    }

    // Function to mint new tokens
    function mint(address to, uint256 amount) external onlyOwner {
        require(to != address(0), "Invalid address");
        require(totalSupply.add(amount) <= TOTAL_SUPPLY_CAP, "Supply cap exceeded");
        totalSupply = totalSupply.add(amount);
        balanceOf[to] = balanceOf[to].add(amount);
        emit TokensMinted(to, amount);
        emit Transfer(address(0), to, amount); // Emit transfer event for minting
    }

    // Function to burn tokens
    function burn(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] = balanceOf[msg.sender].sub(amount);
        totalSupply = totalSupply.sub(amount);
        emit TokensBurned(msg.sender, amount);
        emit Transfer(msg.sender, address(0), amount); // Emit transfer event for burning
    }

    // Function to adjust the supply based on market conditions
    function adjustSupply() external onlyOwner {
        uint256 marketPrice = priceFeed.getLatestPrice();
        if (marketPrice < STABLE_VALUE) {
            // Mint more tokens if the market price is below the stable value
            uint256 amountToMint = STABLE_VALUE.sub(marketPrice).mul(totalSupply).div(marketPrice);
            mint(msg.sender, amountToMint);
        } else if (marketPrice > STABLE_VALUE) {
            // Burn tokens if the market price is above the stable value
            uint256 amountToBurn = marketPrice.sub(STABLE_VALUE).mul(totalSupply).div(marketPrice);
            burn(amountToBurn);
        }
        emit ValueAdjusted(marketPrice);
    }

    // Function to get the current price of the stablecoin
    function getCurrentPrice() external view returns (uint256) {
        return priceFeed.getLatestPrice();
    }

    // Function to get the balance of an account
    function balanceOfAccount(address account) external view returns (uint256) {
        return balanceOf[ account];
    }

    // Function to get the total supply of the stablecoin
    function getTotalSupply() external view returns (uint256) {
        return totalSupply;
    }

    // Function to withdraw Ether from the contract (if any)
    function withdrawEther() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    // Function to withdraw ERC20 tokens from the contract
    function withdrawTokens(address tokenAddress, uint256 amount) external onlyOwner {
        require(tokenAddress != address(this), "Cannot withdraw the stablecoin itself");
        IERC20(tokenAddress).transfer(owner(), amount);
    }
}

// Interface for ERC20 token standard
interface IERC20 {
    function transfer(address recipient, uint256 amount) external returns (bool);
}
