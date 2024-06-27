# node_manager.py
import asyncio
import json
from typing import Dict, List

class NodeManager:
    def __init__(self):
        self.nodes: Dict[str, dict] = {}  # Node ID -> Node info
        self.event_loop = asyncio.get_event_loop()

    async def add_node(self, node_id: str, node_info: dict):
        self.nodes[node_id] = node_info
        await self.broadcast_node_update(node_id, node_info)

    async def remove_node(self, node_id: str):
        if node_id in self.nodes:
            del self.nodes[node_id]
            await self.broadcast_node_update(node_id, None)

    async def broadcast_node_update(self, node_id: str, node_info: dict):
        # Implement broadcasting mechanism using WebSockets or another technology
        pass

    async def get_nodes(self) -> List[dict]:
        return list(self.nodes.values())

node_manager = NodeManager()
