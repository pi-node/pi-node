# node_monitor.py
import psutil
from datetime import datetime

class NodeMonitor:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.cpu_usage: float = 0.0
        self.mem_usage: float = 0.0
        self.disk_usage: float = 0.0
        self.last_update: datetime = datetime.now()

    def update_metrics(self) -> None:
        self.cpu_usage = psutil.cpu_percent()
        self.mem_usage = psutil.virtual_memory().percent
        self.disk_usage = psutil.disk_usage('/').percent
        self.last_update = datetime.now()

    def get_metrics(self) -> Dict:
        return {
            'cpu_usage': self.cpu_usage,
            'mem_usage': self.mem_usage,
            'disk_usage': self.disk_usage,
            'last_update': self.last_update.isoformat()
        }
