pragma solidity ^0.8.0;

contract NFTsMarketplace {
    address private owner;
    mapping (address => uint256) public balances;

    constructor() {
        owner = msg.sender;
    }

    function createNFT(string memory _name, string memory _description, uint256 _price) public {
        // Create a new NFT
    }

    function buyNFT(uint256 _nftId) public payable {
        // Buy an existing NFT
    }

    function sellNFT(uint256 _nftId, uint256 _price) public {
        // Sell an existing NFT
    }
}
