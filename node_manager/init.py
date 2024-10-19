import logging
import os
import json
from node_controller import NodeController
from node_monitor import NodeMonitor
from node_registry import NodeRegistry

# Configure logging
logging.basicConfig(filename='init.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SupernodeInitializer:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.node_controller = NodeController(uri=self.config.get('controller_uri', 'ws://localhost:8765'))
        self.node_monitor = NodeMonitor(uri=self.config.get('monitor_uri', 'ws://localhost:8765'))
        self.node_registry = NodeRegistry(uri=self.config.get('registry_uri', 'ws://localhost:8765'))

    def load_config(self):
        """Load configuration from a JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                logging.info("Configuration loaded successfully.")
                return config
        else:
            logging.error(f"Configuration file {self.config_file} not found. Using default settings.")
            return {}

    def run(self):
        """Run the Supernode components."""
        try:
            logging.info("Starting Supernode components...")
            self.node_registry.run()
            self.node_monitor.run()
            self.node_controller.run()
        except Exception as e:
            logging.error(f"Error while running Supernode components: {e}")

if __name__ == "__main__":
    initializer = SupernodeInitializer()
    initializer.run()
