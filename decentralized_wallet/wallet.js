const ipfs = require('ipfs-api');
const ethers = require('ethers');

const ipfsApi = ipfs('https://ipfs.infura.io:5001');

const wallet = new ethers.Wallet('0x1234567890abcdef');

ipfsApi.add(wallet.privateKey).then((hash) => {
  console.log(`Wallet stored at IPFS hash: ${hash}`);
});
