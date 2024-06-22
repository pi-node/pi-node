# resource_allocator.py
import numpy as np

class ResourceAllocator:
    def __init__(self, node_id: str, node_profiler: NodeProfiler):
        self.node_id = node_id
        self.node_profiler = node_profiler
        self.resources: Dict[str, float] = {}

    def allocate_resources(self, features: Dict[str, float]) -> None:
        predicted_usage = self.node_profiler.predict_usage(features)
        self.resources['cpu'] = predicted_usage * 0.8
        self.resources['mem'] = predicted_usage * 0.2
        self.resources['disk'] = predicted_usage * 0.1

    def get_resources(self) -> Dict[str, float]:
        return self.resources
