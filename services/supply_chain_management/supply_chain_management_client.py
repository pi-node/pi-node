import web3

class SupplyChainManagementClient:
    def __init__(self, contract_address, abi):
        self.contract_address = contract_address
        self.abi = abi
        self.w3 = web3.Web3(web3.providers.HttpProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))

    def register_product(self, address, product):
        # Send request to register a product
        contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        tx_hash = contract.functions.registerProduct(address, product).transact()
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt.status

    def track_product(self, address, product):
        # Send request to track a product
        contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        tx_hash = contract.functions.trackProduct(address, product).transact()
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt.status

    def verify_product(self, address, product):
        # Send request to verify a product
        contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        tx_hash = contract.functions.verifyProduct(address, product).transact()
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt.status
