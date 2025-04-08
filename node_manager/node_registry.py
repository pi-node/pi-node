import asyncio
import logging
import json
import websockets

# Configure logging
logging.basicConfig(filename='node_registry.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NodeRegistry:
    def __init__(self, uri='ws://localhost:8765'):
        self.uri = uri
        self.nodes = {}

    async def connect(self):
        """Establish a WebSocket connection to the node."""
        try:
            async with websockets.connect(self.uri) as websocket:
                logging.info(f"Connected to {self.uri}")
                await self.listen(websocket)
        except Exception as e:
            logging.error(f"Connection error: {e}")

    async def listen(self, websocket):
        """Listen for messages from the WebSocket."""
        while True:
            try:
                message = await websocket.recv()
                logging.info(f"Received message: {message}")
                await self.handle_message(message, websocket)
            except websockets.ConnectionClosed:
                logging.info("Connection closed.")
                break
            except Exception as e:
                logging.error(f"Error while listening: {e}")

    async def handle_message(self, message, websocket):
        """Handle incoming messages for node registration and deregistration."""
        try:
            data = json.loads(message)
            action = data.get('action')
            node_id = data.get('node_id')

            if action == 'register' and node_id:
                await self.register_node(node_id)
            elif action == 'deregister' and node_id:
                await self.deregister_node(node_id)
            else:
                logging.error("Invalid message format or action.")
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON message.")

    async def register_node(self, node_id):
        """Register a new node."""
        if node_id not in self.nodes:
            self.nodes[node_id] = {'status': 'active'}
            logging.info(f"Node {node_id} registered successfully.")
            # Notify other nodes or systems if necessary
        else:
            logging.warning(f"Node {node_id} is already registered.")

    async def deregister_node(self, node_id):
        """Deregister an existing node."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            logging.info(f"Node {node_id} deregistered successfully.")
            # Notify other nodes or systems if necessary
        else:
            logging.warning(f"Node {node_id} not found for deregistration.")

    def run(self):
        """Run the Node Registry."""
        asyncio.run(self.connect())

if __name__ == "__main__":
    node_registry = NodeRegistry()
    node_registry.run()
