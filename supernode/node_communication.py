# node_communication.py
import asyncio
import websockets

class NodeCommunication:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(f"wss://supernode.example.com/{self.node_id}")

    async def send_message(self, message: str):
        await self.websocket.send(message)

    async def receive_message(self):
        return await self.websocket.recv()

node_communication = NodeCommunication("node-1")
asyncio.run(node_communication.connect())
