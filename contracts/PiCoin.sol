// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract PiCoin is Ownable {
    using SafeMath for uint256;

    string public name = "Pi Coin";
    string public symbol = "Pi";
    uint8 public decimals = 18;
    uint256 public constant STABLE_VALUE = 314159 * 10 ** 18; // $314,159 in wei
    uint256 public constant TOTAL_SUPPLY_CAP = 100000000000 * 10 ** 18; // 100 billion tokens
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Mint(address indexed to, uint256 amount);
    event Burn(address indexed from, uint256 amount);

    constructor() {
        totalSupply = 0; // Start with zero total supply
    }

    // Function to mint new tokens
    function mint(address to, uint256 amount) external onlyOwner {
        require(to != address(0), "Invalid address");
        require(amount > 0, "Amount must be greater than zero");
        require(totalSupply.add(amount) <= TOTAL_SUPPLY_CAP, "Supply cap exceeded");

        totalSupply = totalSupply.add(amount);
        balanceOf[to] = balanceOf[to].add(amount);
        emit Mint(to, amount);
        emit Transfer(address(0), to, amount); // Emit transfer event for minting
    }

    // Function to burn tokens
    function burn(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        require(amount > 0, "Amount must be greater than zero");

        balanceOf[msg.sender] = balanceOf[msg.sender].sub(amount);
        totalSupply = totalSupply.sub(amount);
        emit Burn(msg.sender, amount);
        emit Transfer(msg.sender, address(0), amount); // Emit transfer event for burning
    }

    // Function to get the current value of Pi Coin
    function getCurrentValue() external pure returns (uint256) {
        return STABLE_VALUE;
    }

    // Function to transfer tokens
    function transfer(address to, uint256 amount) external returns (bool) {
        require(to != address(0), "Invalid address");
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        require(amount > 0, "Amount must be greater than zero");

        balanceOf[msg.sender] = balanceOf[msg.sender].sub(amount);
        balanceOf[to] = balanceOf[to].add(amount);
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    // Function to approve token spending
    function approve(address spender, uint256 amount) external returns (bool) {
        require(spender != address(0), "Invalid address");
        require(amount > 0, "Amount must be greater than zero");

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
}
