# node_optimizer.py
import numpy as np
from sklearn.cluster import KMeans

class NodeOptimizer:
    def __init__(self, nodes: List[dict]):
        self.nodes = nodes
        self.cluster_model = KMeans(n_clusters=5)  # Adjust the number of clusters as needed

    def optimize_nodes(self) -> List[dict]:
        node_features = np.array([[node['cpu_usage'], node['memory_usage']] for node in self.nodes])
        cluster_labels = self.cluster_model.fit_predict(node_features)
        optimized_nodes = []
        for node, label in zip(self.nodes, cluster_labels):
            node['cluster_label'] = label
            optimized_nodes.append(node)
        return optimized_nodes

node_optimizer = NodeOptimizer(node_manager.get_nodes())
optimized_nodes = node_optimizer.optimize_nodes()
