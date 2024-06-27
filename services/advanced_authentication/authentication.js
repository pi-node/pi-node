const Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'));

const authenticationContract = new web3.eth.Contract([
  {
    constant: true,
    inputs: [],
    name: 'authenticateNode',
    outputs: [{ name: '', type: 'bool' }],
    payable: false,
    stateMutability: 'view',
    type: 'function',
  },
], '0x1234567890abcdef');

const authenticateNode = async (nodeId) => {
  const response = await authenticationContract.methods.authenticateNode(nodeId).call();
  if (response) {
    console.log(`Node ${nodeId} authenticated successfully`);
  } else {
    console.log(`Node ${nodeId} authentication failed`);
  }
};
