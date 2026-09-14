import asyncio
import logging
import json
import websockets
import time

# Configure logging
logging.basicConfig(filename='node_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NodeMonitor:
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
                await self.handle_message(message)
            except websockets.ConnectionClosed:
                logging.info("Connection closed.")
                break
            except Exception as e:
                logging.error(f"Error while listening: {e}")

    async def handle_message(self, message):
        """Handle incoming messages and update node statuses."""
        try:
            data = json.loads(message)
            node_id = data.get('node_id')
            status = data.get('status')

            if node_id and status:
                self.nodes[node_id] = status
                logging.info(f"Updated status for node {node_id}: {status}")
            else:
                logging.error("Invalid message format.")
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON message.")

    def display_statuses(self):
        """Display the current statuses of all monitored nodes."""
        while True:
            print("\nCurrent Node Statuses:")
            for node_id, status in self.nodes.items():
                print(f"Node ID: {node_id}, Status: {status}")
            time.sleep(5)  # Update every 5 seconds

    def run(self):
        """Run the Node Monitor."""
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.connect())
        except KeyboardInterrupt:
            logging.info("Monitor stopped by user.")
        finally:
            loop.close()
            logging.info("Monitor closed.")

if __name__ == "__main__":
    node_monitor = NodeMonitor()
    # Run the display_statuses in a separate thread
    asyncio.run(node_monitor.connect())
    node_monitor.display_statuses()
