# node_profiler.py
import psutil
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class NodeProfiler:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.metrics: Dict[str, List[float]] = {}

    def collect_metrics(self) -> None:
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        self.metrics['cpu_usage'].append(cpu_usage)
        self.metrics['mem_usage'].append(mem_usage)
        self.metrics['disk_usage'].append(disk_usage)

    def train_model(self) -> None:
        df = pd.DataFrame(self.metrics)
        self.model = RandomForestRegressor()
        self.model.fit(df.drop('cpu_usage', axis=1), df['cpu_usage'])

    def predict_usage(self, features: Dict[str, float]) -> float:
        return self.model.predict([features])[0]
