# node_registry.py
import os
import json
from typing import Dict, List

class NodeRegistry:
    def __init__(self, registry_file: str = 'node_registry.json'):
        self.registry_file = registry_file
        self.nodes: Dict[str, Dict] = self.load_registry()

    def load_registry(self) -> Dict[str, Dict]:
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_registry(self) -> None:
        with open(self.registry_file, 'w') as f:
            json.dump(self.nodes, f, indent=4)

    def register_node(self, node_id: str, node_info: Dict) -> None:
        self.nodes[node_id] = node_info
        self.save_registry()

    def get_node(self, node_id: str) -> Dict:
        return self.nodes.get(node_id)

    def get_all_nodes(self) -> List[Dict]:
        return list(self.nodes.values())

    def update_node(self, node_id: str, node_info: Dict) -> None:
        if node_id in self.nodes:
            self.nodes[node_id].update(node_info)
            self.save_registry()

    def remove_node(self, node_id: str) -> None:
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.save_registry()
