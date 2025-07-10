import asyncio
import logging
import json
import websockets

# Configure logging
logging.basicConfig(filename='node_controller.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NodeController:
    def __init__(self, uri='ws://localhost:8765'):
        self.uri = uri

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
        """Handle incoming messages and respond accordingly."""
        try:
            data = json.loads(message)
            response = await self.process_request(data)
            await self.send_response(response, websocket)
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON message.")
            await self.send_response({"error": "Invalid JSON"}, websocket)

    async def process_request(self, data):
        """Process the incoming request and generate a response."""
        if 'command' in data:
            command = data['command']
            logging.info(f"Processing command: {command}")
            # Example command handling
            if command == "status":
                return {"status": "success", "message": "Node is operational."}
            elif command == "shutdown":
                return {"status": "success", "message": "Shutting down."}
            else:
                return {"error": "Unknown command"}
        return {"error": "No command provided"}

    async def send_response(self, response, websocket):
        """Send a response back to the client."""
        response_message = json.dumps(response)
        await websocket.send(response_message)
        logging.info(f"Sent response: {response}")

    def run(self):
        """Run the Node Controller."""
        asyncio.run(self.connect())

if __name__ == "__main__":
    node_controller = NodeController()
    node_controller.run()
