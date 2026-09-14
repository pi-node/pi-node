const Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'));

const reputationContract = new web3.eth.Contract([
  {
    constant: true,
    inputs: [],
    name: 'getNodeReputation',
    outputs: [{ name: '', type: 'uint256' }],
    payable: false,
    stateMutability: 'view',
    type: 'function',
  },
], '0x1234567890abcdef');

const getNodeReputation = async (nodeId) => {
  const response = await reputationContract.methods.getNodeReputation(nodeId).call();
  console.log(`Node ${nodeId} reputation: ${response}`);
};
