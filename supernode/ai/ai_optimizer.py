import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class AIOptimizer:
    def __init__(self, node_data):
        self.node_data = node_data
        self.model = RandomForestRegressor(n_estimators=100)

    def train_model(self):
        X = np.array(self.node_data['cpu_usage'])
        y = np.array(self.node_data['memory_usage'])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    def predict_optimal_config(self, node_id):
        cpu_usage = self.node_data[node_id]['cpu_usage']
        memory_usage = self.model.predict(cpu_usage)
        return {'cpu_usage': cpu_usage, 'memory_usage': memory_usage}

    def optimize_node(self, node_id):
        optimal_config = self.predict_optimal_config(node_id)
        # Apply optimal configuration to the node
        print(f"Optimized node {node_id} with config: {optimal_config}")
