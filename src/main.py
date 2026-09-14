import logging
import time
from config import Config
from blockchain import Blockchain
from node import Node
from transaction import TransactionPool
from api import API
from consensus import Consensus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PiNode:
    def __init__(self):
        self.config = Config()
        self.blockchain = Blockchain()
        self.node = Node(self.config)
        self.transaction_pool = TransactionPool()
        self.api = API(self.config, self.blockchain, self.transaction_pool)
        self.consensus = Consensus(self.blockchain)

    def start(self):
        logger.info("Starting Pi Node...")
        self.node.start()  # Start the node's networking capabilities
        self.api.start()   # Start the API server

        try:
            while True:
                self.consensus.run()  # Run the consensus algorithm
                time.sleep(self.config.CONSENSUS_INTERVAL)  # Wait before the next consensus round
        except KeyboardInterrupt:
            logger.info("Shutting down Pi Node...")
            self.node.stop()
            self.api.stop()

if __name__ == "__main__":
    pi_node = PiNode()
    pi_node.start()
